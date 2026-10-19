import hashlib
import os
from dotenv import load_dotenv
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix


def _is_development() -> bool:
    return os.environ.get("FLASK_ENV") == "development"


def create_app():
    load_dotenv()

    # Allow HTTP for local development (Google OAuth requires HTTPS in production)
    if _is_development():
        os.environ.setdefault("OAUTHLIB_INSECURE_TRANSPORT", "1")

    app = Flask(__name__)

    secret_key = os.environ.get("FLASK_SECRET_KEY")
    if not secret_key and not _is_development():
        raise RuntimeError("FLASK_SECRET_KEY is not set: sessions (and Google login) cannot work without it.")
    app.secret_key = secret_key

    # Behind a reverse proxy (Vercel, Cloud Run, nginx…) the app receives plain HTTP: trust the
    # X-Forwarded-* headers so request.url is https:// and the OAuth callback is accepted.
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

    if not _is_development():
        app.config.update(
            SESSION_COOKIE_SECURE=True,
            SESSION_COOKIE_HTTPONLY=True,
            SESSION_COOKIE_SAMESITE="Lax",  # Lax keeps the cookie on Google's redirect back to /login/callback
            SEND_FILE_MAX_AGE_DEFAULT=60 * 60 * 24 * 365,  # static URLs are versioned (see below)
        )

    # Server-side cache for credentials/events. Serverless hosts run many short-lived instances,
    # so the in-memory fallback would lose the login between requests: require Redis there.
    from web_app.CacheManager import CacheManager
    redis_url = os.environ.get("REDIS_URL") or os.environ.get("KV_URL")
    if redis_url:
        CacheManager.init_redis(redis_url=redis_url)
    elif os.environ.get("VERCEL"):
        raise RuntimeError("REDIS_URL is not set: on Vercel a Redis store (e.g. Upstash) is required to keep users logged in.")

    # Blueprints
    from web_app.routes.login import bp as login
    app.register_blueprint(login)

    from web_app.routes.home import bp as main
    app.register_blueprint(main)

    from web_app.routes.new_events import bp as new_events
    app.register_blueprint(new_events)

    from web_app.routes.get_events import bp as get_events
    app.register_blueprint(get_events)

    from web_app.routes.edit_events import bp as edit_events
    app.register_blueprint(edit_events)

    from web_app.routes.graph_viewer import bp as graph_viewer
    app.register_blueprint(graph_viewer)

    # Cache-busting: url_for('static', ...) gets ?v=<content hash> so browsers pick up CSS/JS changes
    # immediately. A content hash (not mtime) stays correct on hosts that reset file timestamps on deploy.
    static_versions: dict[str, str] = {}

    @app.url_defaults
    def static_cache_buster(endpoint, values):
        if endpoint != "static" or "filename" not in values or "v" in values:
            return
        filename = values["filename"]
        if filename not in static_versions or _is_development():
            path = os.path.join(app.static_folder, filename)
            if not os.path.isfile(path):
                return
            with open(path, "rb") as f:
                static_versions[filename] = hashlib.md5(f.read(), usedforsecurity=False).hexdigest()[:10]
        values["v"] = static_versions[filename]

    # Signed-in Google profile (set at login) available to every template as `current_user`
    from flask import session

    @app.context_processor
    def inject_current_user():
        return {"current_user": session.get("user")}

    # Error handlers
    from web_app.routes import error_page
    error_page.register_error_handlers(app)

    return app
