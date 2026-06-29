from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, session, url_for
import markdown
from google.oauth2.credentials import Credentials

from common.CommonOperations import CommonOperations
from common.InformationMessages import InformationMessages
from common.ConfigKeys import ConfigKeys
from common.entities.EventInfo import EventInfo
from common.entities.TimeRange import TimeRange
from common.services.EventsService import EventsService
from common.settings import TIMEZONE
from web_app.CacheManager import CacheManager
from web_app.services.validate import Validate

bp = Blueprint("edit_events", __name__, url_prefix="/edit-events")


def _render_page(form_values=None, old_events=None, new_event=None, show_confirm_modal=False):
    return render_template(
        "edit-events.html",
        active_page="edit events",
        section_message=markdown.markdown(InformationMessages.get_events_info_message, extensions=["extra", "nl2br"]),
        event_colors_old=ConfigKeys.Keys.EVENT_COLOR.value,
        event_colors_new=ConfigKeys.Keys.EVENT_COLOR.value,
        timezones=TIMEZONE,
        old_events=old_events or [],
        new_event=new_event,
        show_confirm_modal=show_confirm_modal,
        form_values=form_values or {},
    )


@bp.route("/", methods=["GET", "POST"])
def edit_events():
    cred_cache_id = session.get("cred_cache_id")
    credentials: Credentials = CacheManager.get(cred_cache_id)
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

            old_event_info = _build_old_event_info(form_values)
            old_events = CommonOperations.get_events(credentials, old_event_info)

            if not old_events:
                flash("No events found for the given criteria.", "info")
                return _render_page(form_values=form_values)

            session["events_cache_id"] = CacheManager.store(old_events)

            color_index_new = CommonOperations.get_color_id(form_values["color_new"])
            time_range_new = TimeRange(datetime.fromisoformat(date_from_str), datetime.fromisoformat(date_to_str))
            new_event_info = EventInfo(
                form_values["summary_new"],
                form_values["description_new"],
                time_range_new,
                color_index_new,
                form_values["timezone"],
            )

            session["pending_update"] = {
                "summary_new": form_values["summary_new"],
                "description_new": form_values["description_new"],
                "color_index_new": color_index_new,
                "date_from": date_from_str,
                "date_to": date_to_str,
                "timezone": form_values["timezone"],
            }

            return _render_page(
                form_values=form_values,
                old_events=old_events,
                new_event=new_event_info,
                show_confirm_modal=True,
            )

        elif action == "update":
            return _confirm_update(credentials)

        elif action == "cancel":
            session.pop("events_cache_id", None)
            session.pop("pending_update", None)
            return redirect(url_for("edit_events.edit_events"))

    return _render_page()


def _build_old_event_info(form_values: dict) -> EventInfo:
    color_index_old = CommonOperations.get_color_id(form_values["color_old"])
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


def _confirm_update(credentials: Credentials):
    pending = session.get("pending_update")
    old_events_cache_id = session.get("events_cache_id")
    old_events = CacheManager.get(old_events_cache_id)

    time_range = TimeRange(pending["date_from"], pending["date_to"])
    event_info = EventInfo(
        pending["summary_new"],
        pending["description_new"],
        time_range,
        pending["color_index_new"],
        pending["timezone"],
    )

    updated_events = EventsService.edit_events(credentials, event_info, old_events)
    flash(f"{len(updated_events)} event(s) successfully updated!", "success")

    session.pop("pending_update", None)
    new_cache_id = CacheManager.store(updated_events)
    session["events_cache_id"] = new_cache_id

    return redirect(url_for("edit_events.edit_events"))