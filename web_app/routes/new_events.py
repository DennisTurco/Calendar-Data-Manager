from datetime import datetime
from flask import Blueprint, flash, json, redirect, render_template, request, session, url_for
from common.CommonOperations import CommonOperations
from common.ConfigKeys import ConfigKeys
from common.entities.EventInfo import EventInfo
from common.entities.TimeRange import TimeRange
from common.services.EventsService import EventsService
from common.settings import TIMEZONE
from common.InformationMessages import InformationMessages
from google.oauth2.credentials import Credentials
import markdown

bp = Blueprint("new_events", __name__, url_prefix="/new-events")

@bp.route("/", methods=["GET", "POST"])
def new_events():

    if request.method == "POST":
        return _create_event()

    return render_template(
        "new-events.html",
        active_page="new events",

        section_message = markdown.markdown(InformationMessages.new_event_info_message, extensions=["extra", "nl2br"]),
        colors = ConfigKeys.Keys.EVENT_COLOR.value,
        timezones = TIMEZONE
        )

def _create_event():
    credentials_json = session.get("google_credentials")

    if not credentials_json:
        flash("Please login with Google first", "error")
        return redirect(url_for("login.login"))

    summary = request.form.get("summary")
    description = request.form.get("description")
    color = request.form.get("color")
    date_from_str = request.form.get("date_from")
    date_to_str = request.form.get("date_to")
    timezone = request.form.get("timezone")

    color_id = CommonOperations.get_color_id(color)

    if not _is_date_provided(date_from_str, date_to_str):
        flash("Please select both start and end dates", "error")
        return redirect(url_for("new_events.new_events"))

    date_from = datetime.fromisoformat(date_from_str)
    date_to = datetime.fromisoformat(date_to_str)

    if not _is_date_interval_valid(date_from, date_to):
        flash("Date Range is not valid", "error")
        return redirect(url_for("new_events.new_events"))

    time_range = TimeRange(date_from, date_to)
    event_info = EventInfo(summary, description, time_range, color_id, timezone)

    credentials = Credentials.from_authorized_user_info(
        json.loads(credentials_json)
    )

    try:
        EventsService.create_event(credentials, event_info)
        flash("Event created successfully", "success")
    except Exception as e:
        flash(f"Error creating event: {e}", "error")

    return redirect(url_for("new_events.new_events"))

def _is_date_provided(date_from_str, date_to_str) -> bool:
    return date_from_str or not date_to_str

def _is_date_interval_valid(date_from: datetime, date_to: datetime) -> bool:
    return date_from < date_to
