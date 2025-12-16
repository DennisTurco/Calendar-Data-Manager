from flask import Blueprint, current_app, redirect, render_template, session, url_for

from common.ConfigKeys import ConfigKeys

bp = Blueprint("main", __name__)

@bp.route("/")
def index():

    if not session.get("google_authenticated"):
        return redirect(url_for("login.login"))
    
    current_app.logger.debug(f"SESSION: {dict(session)}")

    return render_template(
        "index.html",
        active_page="home",
        
        show_msg_section=ConfigKeys.Keys.HOMEBUTTONS_MESSAGESECTION,
        show_github=ConfigKeys.Keys.HOMEBUTTONS_GITHUB,
        show_buymeacoffee=ConfigKeys.Keys.HOMEBUTTONS_BUYMEACOFFE,
        show_paypal=ConfigKeys.Keys.HOMEBUTTONS_PAYPAL,
        
        github_link=ConfigKeys.Keys.GITHUB_PAGE_LINK.value,
        buymeacoffee_link=ConfigKeys.Keys.DONATE_BUYMEACOFFE_PAGE_LINK.value,
        paypal_link=ConfigKeys.Keys.DONATE_PAYPAL_PAGE_LINK.value,

        version=ConfigKeys.Keys.VERSION.value
        )
