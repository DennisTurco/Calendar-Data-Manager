from flask import Blueprint, render_template
import markdown

from common.InformationMessages import InformationMessages
from common.ConfigKeys import ConfigKeys
from common.settings import TIMEZONE

bp = Blueprint("get_events", __name__, url_prefix="/get-events")

@bp.route("/")
def get_events():
    return render_template(
        "get-events.html",
        active_page="get events",

        section_message = markdown.markdown(InformationMessages.get_events_info_message, extensions=["extra", "nl2br"]),
        event_colors = ConfigKeys.Keys.EVENT_COLOR.value,
        timezones = TIMEZONE
        )
