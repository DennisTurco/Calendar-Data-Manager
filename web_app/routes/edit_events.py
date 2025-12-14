from flask import Blueprint, render_template
import markdown

from common.InformationMessages import InformationMessages
from common.ConfigKeys import ConfigKeys
from common.settings import TIMEZONE

bp = Blueprint("edit_events", __name__, url_prefix="/edit-events")

@bp.route("/")
def edit_events():
    return render_template(
        "edit-events.html",
        active_page="edit events",
        
        section_message = markdown.markdown(InformationMessages.get_events_info_message, extensions=["extra", "nl2br"]),
        event_colors_old = ConfigKeys.Keys.EVENT_COLOR.value,
        event_colors_new = ConfigKeys.Keys.EVENT_COLOR.value,
        timezones = TIMEZONE
        )
