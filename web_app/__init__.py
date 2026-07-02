import os
from dotenv import load_dotenv
from flask import Flask


def create_app():
    load_dotenv()

    # Allow HTTP for local development (Google OAuth requires HTTPS in production)
    if os.environ.get("FLASK_ENV") == "development":
        os.environ.setdefault("OAUTHLIB_INSECURE_TRANSPORT", "1")

    app = Flask(__name__)
    app.secret_key = os.environ.get("FLASK_SECRET_KEY")

    # Redis cache (optional — falls back to in-memory when REDIS_URL is not set)
    from web_app.CacheManager import CacheManager
    redis_url = os.environ.get("REDIS_URL")
    if redis_url:
        CacheManager.init_redis(redis_url=redis_url)

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

    # Error handlers
    from web_app.routes import error_page
    error_page.register_error_handlers(app)

    return app
