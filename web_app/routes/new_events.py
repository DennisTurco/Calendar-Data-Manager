from flask import Blueprint, render_template
from common.ConfigKeys import ConfigKeys
from common.settings import TIMEZONE
from common.InformationMessages import InformationMessages
import markdown

bp = Blueprint("new-events", __name__, url_prefix="/new-events")

@bp.route("/")
def new_events():
    return render_template(
        "new-events.html",
        active_page="new events",

        section_message = markdown.markdown(InformationMessages.new_event_info_message, extensions=["extra", "nl2br"]),
        colors = ConfigKeys.Keys.EVENT_COLOR.value,
        timezones = TIMEZONE
        )
