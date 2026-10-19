import os
from flask import Blueprint, current_app, render_template, session, redirect, url_for, flash, request
from google_auth_oauthlib.flow import Flow
from web_app.CacheManager import CacheManager

bp = Blueprint("login", __name__, url_prefix="/login")

_USERINFO_URL = "https://openidconnect.googleapis.com/v1/userinfo"

_SCOPES = [
    "https://www.googleapis.com/auth/calendar",
    "openid",
    "https://www.googleapis.com/auth/userinfo.email",
    "https://www.googleapis.com/auth/userinfo.profile",
]


def _build_flow(state: str = None) -> Flow:
    client_config = {
        "web": {
            "client_id": os.environ["GOOGLE_CLIENT_ID"],
            "client_secret": os.environ["GOOGLE_CLIENT_SECRET"],
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
        }
    }
    flow = Flow.from_client_config(client_config, scopes=_SCOPES, state=state)
    flow.redirect_uri = os.environ["GOOGLE_REDIRECT_URI"]
    return flow


@bp.route("/", methods=["GET"])
def login():
    return render_template("login.html")


@bp.route("/google-auth", methods=["GET"])
def google_auth():
    flow = _build_flow()
    authorization_url, state = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )
    session["oauth_state"] = state
    return redirect(authorization_url)


@bp.route("/callback", methods=["GET"])
def callback():
    if "error" in request.args:
        flash(f"Login failed: {request.args.get('error')}", "error")
        return redirect(url_for("login.login"))

    try:
        flow = _build_flow(state=session.get("oauth_state"))
        flow.fetch_token(authorization_response=request.url)
        credentials = flow.credentials
    except Exception as e:
        flash(f"Authentication error: {e}", "error")
        return redirect(url_for("login.login"))

    user = _fetch_user_profile(flow)

    session.clear()
    session["google_authenticated"] = True
    session["cred_cache_id"] = CacheManager.store(credentials, ttl=3600)
    if user:
        session["user"] = user

    return redirect(url_for("main.index"))


def _fetch_user_profile(flow: Flow) -> dict | None:
    """Name, email and avatar of the signed-in Google account (openid/profile/email scopes)."""
    try:
        resp = flow.authorized_session().get(_USERINFO_URL, timeout=10)
        resp.raise_for_status()
        info = resp.json()
    except Exception as e:
        current_app.logger.warning(f"Could not fetch Google user profile: {e}")
        return None
    return {
        "name": info.get("name") or info.get("given_name") or info.get("email", ""),
        "email": info.get("email", ""),
        "picture": info.get("picture", ""),
    }


@bp.route("/logout", methods=["GET"])
def logout():
    cred_cache_id = session.get("cred_cache_id")
    if cred_cache_id:
        CacheManager.delete(cred_cache_id)
    session.clear()
    return redirect(url_for("login.login"))
