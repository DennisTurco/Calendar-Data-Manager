from collections import defaultdict
from datetime import datetime
from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for
import markdown
from google.oauth2.credentials import Credentials

from common.CommonOperations import CommonOperations
from common.InformationMessages import InformationMessages
from common.ConfigKeys import ConfigKeys
from common.entities.EventInfo import EventInfo
from common.entities.TimeRange import TimeRange
from common.enums.GraphType import GraphType
from common.settings import TIMEZONE
from web_app.CacheManager import CacheManager
from web_app.services.validate import Validate

bp = Blueprint("get_events", __name__, url_prefix="/get-events")


def _render_page(form_values=None, summary_totals=None, total_events=None, grand_total_hours=0.0):
    return render_template(
        "get-events.html",
        active_page="get events",
        section_message=markdown.markdown(
            InformationMessages.get_events_info_message,
            extensions=["extra", "nl2br"]
        ),
        event_colors=ConfigKeys.Keys.EVENT_COLOR.value,
        timezones=TIMEZONE,
        graph_types=GraphType.to_list(),
        form_values=form_values or {},
        summary_totals=summary_totals,
        total_events=total_events,
        grand_total_hours=grand_total_hours,
    )


@bp.route("/", methods=["GET", "POST"])
def get_events():
    cred_cache_id = session.get("cred_cache_id")
    credentials: Credentials = CacheManager.get(cred_cache_id)
    if not credentials:
        return redirect(url_for("login.login"))

    if request.method == "POST":
        return _handle_post(credentials)

    return _render_page()


def _handle_post(credentials: Credentials):
    summary = request.form.get("summary", "")
    description = request.form.get("description", "")
    color = request.form.get("color", "")
    timezone = request.form.get("timezone", "")
    date_from_str = request.form.get("date_from", "")
    date_to_str = request.form.get("date_to", "")
    action = request.form.get("action", "get_and_plot")

    form_values = {
        "summary": summary,
        "description": description,
        "color": color,
        "timezone": timezone,
        "date_from": date_from_str,
        "date_to": date_to_str,
    }
    # Preserve checkbox state for graph types
    for key in request.form.keys():
        if key.replace("_", " ") in GraphType.to_list():
            form_values[key] = request.form.get(key)

    if not Validate.is_date_provided_valid(date_from_str, date_to_str):
        flash("Please select both start and end dates", "error")
        return _render_page(form_values=form_values)

    date_from = datetime.fromisoformat(date_from_str)
    date_to = datetime.fromisoformat(date_to_str)

    if not Validate.is_date_interval_valid(date_from, date_to):
        flash("Date Range is not valid", "error")
        return _render_page(form_values=form_values)

    time_range = TimeRange(date_from, date_to)
    color_index = CommonOperations.get_color_id(color)
    event_info = EventInfo(summary, description, time_range, color_index, timezone)

    if action == "get_list":
        events = CommonOperations.get_events(credentials, event_info)
        if not events:
            flash("No events found for the given criteria.", "info")
            return _render_page(form_values=form_values)

        summary_totals, grand_total_hours = _compute_summary_totals(events)
        flash(f"{len(events)} event(s) found.", "success")
        return _render_page(
            form_values=form_values,
            summary_totals=summary_totals,
            total_events=len(events),
            grand_total_hours=grand_total_hours,
        )

    # action == "get_and_plot"
    selected_graphs = [
        key.replace("_", " ") for key in request.form.keys()
        if key.replace("_", " ") in GraphType.to_list() and request.form.get(key)
    ]

    if not selected_graphs:
        flash("Please select at least one graph type", "error")
        return _render_page(form_values=form_values)

    events = CommonOperations.get_events(credentials, event_info)

    if not events:
        flash("No events found for the given criteria.", "info")
        return _render_page(form_values=form_values)

    cache_id = CacheManager.store(events)
    session["selected_graphs"] = selected_graphs
    session["events_cache_id"] = cache_id

    current_app.logger.debug(f"SESSION: {dict(session)}")
    return redirect(url_for("graph_viewer.view_graphs"))


def _compute_summary_totals(events: list) -> tuple:
    """Group events by summary, returning (list_of_totals, grand_total_hours)."""
    totals = defaultdict(lambda: {"count": 0, "total_minutes": 0.0})

    for event in events:
        summary_name = event.get("summary") or "(no summary)"
        start = event.get("start", {})
        end = event.get("end", {})
        start_val = start.get("dateTime") or start.get("date")
        end_val = end.get("dateTime") or end.get("date")

        totals[summary_name]["count"] += 1

        if start_val and end_val:
            try:
                s = datetime.fromisoformat(start_val.replace("Z", "+00:00"))
                e = datetime.fromisoformat(end_val.replace("Z", "+00:00"))
                duration_minutes = (e - s).total_seconds() / 60
                totals[summary_name]["total_minutes"] += duration_minutes
            except Exception:
                pass

    result = []
    grand_minutes = 0.0
    for name, data in totals.items():
        mins = data["total_minutes"]
        grand_minutes += mins
        h = int(mins // 60)
        m = int(mins % 60)
        result.append({
            "summary": name,
            "count": data["count"],
            "total_hours": mins / 60,
            "duration_str": f"{h}h {m:02d}m" if h > 0 else f"{m}m",
        })

    result.sort(key=lambda x: x["total_hours"], reverse=True)
    grand_total_hours = grand_minutes / 60
    return result, grand_total_hours

