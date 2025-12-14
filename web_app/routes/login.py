import os
from flask import Blueprint, render_template, session, redirect, url_for, flash, request
from common.CommonOperations import CommonOperations
from common.JsonPreferences import JsonPreferences
from common.services.EventsService import EventsService

bp = Blueprint("login", __name__, url_prefix="/login")

@bp.route("/", methods=["GET"])
def login():
    return render_template("login.html")

@bp.route("/google-login", methods=["POST"])
def google_login():
    common = CommonOperations()
    event_service = EventsService(common)

    list_res = JsonPreferences.read_from_json()

    if not isinstance(list_res, dict) or len(list_res) <= 0:
        flash("No credentials configuration found.")
        return redirect(url_for("login.login"))

    credentials_path = list_res.get("CredentialsPath", "./settings/client.json")
    token_path = list_res.get("TokenPath", credentials_path.rsplit("/", 1)[0] + "/token.json")

    try:
        credentials = event_service.get_connection_setup(credentials_path, token_path)
        if credentials:
            session["google_authenticated"] = True
            return redirect(url_for("main.index"))
        else:
            flash("Login failed. Please retry.")
            return redirect(url_for("login.login"))
    except Exception as e:
        # rimuovi token scaduto/invalidato
        try:
            os.remove(token_path)
        except FileNotFoundError:
            pass
        flash(f"Credentials error: {e}")
        return redirect(url_for("login.login"))