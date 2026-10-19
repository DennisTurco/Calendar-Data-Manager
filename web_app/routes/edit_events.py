import hashlib
from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, url_for
import markdown
from google.oauth2.credentials import Credentials

from common.services.EventQueries import EventQueries
from common.InformationMessages import InformationMessages
from common.ConfigKeys import ConfigKeys
from common.entities.EventInfo import EventInfo
from common.entities.TimeRange import TimeRange
from common.services.EventsService import EventsService
from common.settings import TIMEZONE
from web_app.services.auth import load_credentials
from web_app.services.validate import Validate
from web_app.services.events_utils import EventsUtils

bp = Blueprint("edit_events", __name__, url_prefix="/edit-events")


def _render_page(form_values=None, old_events=None, new_event=None, show_confirm_modal=False, no_results=False, fingerprint=""):
    form_values = form_values or {}
    return render_template(
        "edit-events.html",
        active_page="edit events",
        section_message=markdown.markdown(InformationMessages.update_events_info_message, extensions=["extra", "nl2br"]),
        event_colors=ConfigKeys.Keys.EVENT_COLOR.value,
        timezones=TIMEZONE,
        preview_rows=_build_preview_rows(old_events or [], form_values) if show_confirm_modal else [],
        new_event=new_event,
        show_confirm_modal=show_confirm_modal,
        no_results=no_results,
        fingerprint=fingerprint,
        form_values=form_values,
    )


def _build_preview_rows(old_events: list, form_values: dict) -> list:
    """Describe, per matched event, what the update will change (mirrors CalendarEventsManager.edit_event)."""
    colors = ConfigKeys.Keys.EVENT_COLOR.value
    color_names = list(colors.keys())
    new_color_name = form_values.get("color_new") or color_names[0]
    rows = []
    for i, ev in enumerate(old_events, start=1):
        start = ev.get("start", {})
        end = ev.get("end", {})
        rows.append({
            "index": i,
            "summary_old": ev.get("summary", ""),
            "summary_new": form_values.get("summary_new", ""),
            "color_old": EventsUtils.event_color(ev.get("colorId")),
            "color_new": {"name": new_color_name, "hex": colors.get(new_color_name)},
            "start": EventsUtils.format_display_datetime(start.get("dateTime") or start.get("date", "")),
            "end": EventsUtils.format_display_datetime(end.get("dateTime") or end.get("date", "")),
        })
    return rows


@bp.route("/", methods=["GET", "POST"])
def edit_events():
    credentials: Credentials = load_credentials()
    if not credentials:
        return redirect(url_for("login.login"))

    if request.method == "POST":
        action = request.form.get("action")

        form_values = {
            "summary_old": request.form.get("summary_old", ""),
            "description_old": request.form.get("description_old", ""),
            "color_old": request.form.get("color_old", ""),
            "summary_new": request.form.get("summary_new", ""),
            "description_new": request.form.get("description_new", ""),
            "color_new": request.form.get("color_new", ""),
            "date_from": request.form.get("date_from", ""),
            "date_to": request.form.get("date_to", ""),
            "timezone": request.form.get("timezone", ""),
        }

        if action == "fetch":
            date_from_str = form_values["date_from"]
            date_to_str = form_values["date_to"]

            if not Validate.is_date_provided_valid(date_from_str, date_to_str):
                flash("Please select both start and end dates", "error")
                return _render_page(form_values=form_values)

            date_from = datetime.fromisoformat(date_from_str)
            date_to = datetime.fromisoformat(date_to_str)
            if not Validate.is_date_interval_valid(date_from, date_to):
                flash("Date Range is not valid", "error")
                return _render_page(form_values=form_values)

            old_events = EventQueries.get_events(credentials, _build_old_event_info(form_values))

            if not old_events:
                return _render_page(form_values=form_values, no_results=True)

            return _render_preview(form_values, old_events)

        elif action == "update":
            return _confirm_update(credentials, form_values)

        elif action == "cancel":
            return redirect(url_for("edit_events.edit_events"))

    return _render_page()


def _build_old_event_info(form_values: dict) -> EventInfo:
    color_index_old = EventQueries.get_color_id(form_values["color_old"])
    time_range = TimeRange(
        datetime.fromisoformat(form_values["date_from"]),
        datetime.fromisoformat(form_values["date_to"]),
    )
    return EventInfo(
        form_values["summary_old"],
        form_values["description_old"],
        time_range,
        color_index_old,
        form_values["timezone"],
    )


def _events_fingerprint(events: list) -> str:
    """Identifies the exact set (and versions) of matched events, to detect changes after the preview."""
    keys = sorted(f"{e.get('id', '')}:{e.get('updated', '')}" for e in events)
    return hashlib.sha256("|".join(keys).encode()).hexdigest()


def _new_event_info(form_values: dict) -> EventInfo:
    return EventInfo(
        form_values["summary_new"],
        form_values["description_new"],
        TimeRange(datetime.fromisoformat(form_values["date_from"]), datetime.fromisoformat(form_values["date_to"])),
        EventQueries.get_color_id(form_values["color_new"]),
        form_values["timezone"],
    )


def _render_preview(form_values: dict, old_events: list):
    # No server-side state: the confirm form posts the same values back (hidden fields) together
    # with a fingerprint of the previewed events, and the search is repeated at confirm time.
    return _render_page(
        form_values=form_values,
        old_events=old_events,
        new_event=_new_event_info(form_values),
        show_confirm_modal=True,
        fingerprint=_events_fingerprint(old_events),
    )


def _confirm_update(credentials: Credentials, form_values: dict):
    try:
        old_events = EventQueries.get_events(credentials, _build_old_event_info(form_values))
    except ValueError:
        flash("Your preview is no longer valid. Please search again.", "error")
        return redirect(url_for("edit_events.edit_events"))

    if not old_events:
        flash("The matching events are gone: nothing was updated.", "info")
        return _render_page(form_values=form_values, no_results=True)

    if _events_fingerprint(old_events) != request.form.get("fingerprint"):
        flash("The matching events changed since your preview. Review them again before confirming.", "info")
        return _render_preview(form_values, old_events)

    updated_events = EventsService.edit_events(credentials, _new_event_info(form_values), old_events)
    flash(f"{len(updated_events or [])} event(s) successfully updated!", "success")
    return redirect(url_for("edit_events.edit_events"))