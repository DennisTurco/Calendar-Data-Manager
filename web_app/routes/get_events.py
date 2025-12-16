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

@bp.route("/", methods=["GET", "POST"])
def get_events():
    if request.method == "POST":
        return _fetch_events()
    
    return render_template(
        "get-events.html",
        active_page="get events",
        section_message=markdown.markdown(
            InformationMessages.get_events_info_message,
            extensions=["extra", "nl2br"]
        ),
        event_colors=ConfigKeys.Keys.EVENT_COLOR.value,
        timezones=TIMEZONE,
        graph_types=GraphType.to_list()
    )


def _fetch_events():
    cred_cache_id = session.get("cred_cache_id")
    credentials: Credentials = CacheManager.get(cred_cache_id)
    if not credentials:
        return redirect(url_for("login.login"))
    
    summary = request.form.get("summary")
    description = request.form.get("description")
    color = request.form.get("color")
    timezone = request.form.get("timezone")
    date_from_str = request.form.get("date_from")
    date_to_str = request.form.get("date_to")

    if not Validate.is_date_provided_valid(date_from_str, date_to_str):
        return _print_error_and_return("Please select both start and end dates")

    date_from = datetime.fromisoformat(date_from_str)
    date_to = datetime.fromisoformat(date_to_str)

    if not Validate.is_date_interval_valid(date_from, date_to):
        return _print_error_and_return("Date Range is not valid")

    selected_graphs = [
        key.replace("_", " ") for key in request.form.keys()
        if key.replace("_", " ") in GraphType.to_list() and request.form.get(key)
    ]

    if not selected_graphs:
        return _print_error_and_return("Please select at least one graph type")

    time_range = TimeRange(date_from, date_to)
    color_index = CommonOperations.get_color_id(color)
    event_info = EventInfo(summary, description, time_range, color_index, timezone)

    events = CommonOperations.get_events(credentials, event_info)

    cache_id = CacheManager.store(events)
    session["selected_graphs"] = selected_graphs
    session["events_cache_id"] = cache_id

    current_app.logger.debug(f"SESSION: {dict(session)}")

    return redirect(url_for("graph_viewer.view_graphs"))


def _print_error_and_return(error_message: str):
    flash(error_message, "error")
    return redirect(url_for("get_events.get_events"))
