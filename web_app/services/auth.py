"""Google credentials kept in the user's own session cookie, encrypted.

The web app is stateless (no Redis or database), so it can run on serverless hosts where every
request may hit a fresh instance. Flask's session cookie is only *signed*, so the OAuth tokens are
additionally encrypted with a key derived from FLASK_SECRET_KEY. The OAuth client id/secret are never
stored in the cookie: they come from the environment when the credentials are rebuilt.
"""
import base64
import hashlib
import json
import os
from datetime import datetime

from cryptography.fernet import Fernet, InvalidToken
from flask import current_app, g, session
from google.oauth2.credentials import Credentials

_SESSION_KEY = "google_creds"
_TOKEN_URI = "https://oauth2.googleapis.com/token"


def _fernet() -> Fernet:
    secret = (current_app.secret_key or "").encode()
    key = hashlib.sha256(b"cdm-google-credentials:" + secret).digest()
    return Fernet(base64.urlsafe_b64encode(key))


def save_credentials(credentials: Credentials) -> None:
    payload = {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "expiry": credentials.expiry.isoformat() if credentials.expiry else None,
        "scopes": list(credentials.scopes or []),
    }
    session[_SESSION_KEY] = _fernet().encrypt(json.dumps(payload).encode()).decode()


def load_credentials() -> Credentials | None:
    """Credentials of the signed-in user, or None when signed out / cookie unreadable."""
    if "credentials" in g:
        return g.credentials

    credentials = None
    blob = session.get(_SESSION_KEY)
    if blob:
        try:
            data = json.loads(_fernet().decrypt(blob.encode()))
            credentials = Credentials(
                token=data["token"],
                refresh_token=data.get("refresh_token"),
                token_uri=_TOKEN_URI,
                client_id=os.environ.get("GOOGLE_CLIENT_ID"),
                client_secret=os.environ.get("GOOGLE_CLIENT_SECRET"),
                scopes=data.get("scopes") or None,
            )
            if data.get("expiry"):
                credentials.expiry = datetime.fromisoformat(data["expiry"])
            g.credentials_token = credentials.token
        except (InvalidToken, ValueError, KeyError, TypeError):
            # Secret key rotated or cookie tampered with: treat as signed out
            session.pop(_SESSION_KEY, None)
            credentials = None

    g.credentials = credentials
    return credentials


def persist_refreshed_credentials(response):
    """after_request hook: Google client libraries refresh expired tokens in place — store the new one."""
    credentials = g.get("credentials")
    if credentials is not None and credentials.token and credentials.token != g.get("credentials_token"):
        save_credentials(credentials)
    return response


def clear_credentials() -> None:
    session.pop(_SESSION_KEY, None)
