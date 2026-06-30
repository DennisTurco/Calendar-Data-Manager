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


def _render_page(form_values=None, events_list=None, total_events=None):
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
        events_list=events_list,
        total_events=total_events,
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

        events_list = _format_events_list(events)
        flash(f"{len(events)} event(s) found.", "success")
        return _render_page(
            form_values=form_values,
            events_list=events_list,
            total_events=len(events),
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


def _format_events_list(events: list) -> list:
    """Return individual event rows matching the desktop viewer format."""
    result = []
    for index, event in enumerate(events, start=1):
        start = event.get("start", {})
        end = event.get("end", {})
        start_val = start.get("dateTime") or start.get("date") or ""
        end_val = end.get("dateTime") or end.get("date") or ""

        duration_str = ""
        if start_val and end_val:
            try:
                s = datetime.fromisoformat(start_val.replace("Z", "+00:00"))
                e = datetime.fromisoformat(end_val.replace("Z", "+00:00"))
                delta = e - s
                total_seconds = int(delta.total_seconds())
                h, remainder = divmod(total_seconds, 3600)
                m, s_sec = divmod(remainder, 60)
                duration_str = f"{h}:{m:02d}:{s_sec:02d}"
            except Exception:
                pass

        result.append({
            "index": index,
            "id": event.get("id", ""),
            "summary": event.get("summary") or "(no summary)",
            "start": start_val,
            "end": end_val,
            "duration": duration_str,
        })
    return result

