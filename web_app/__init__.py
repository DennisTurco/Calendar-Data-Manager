import os
from dotenv import load_dotenv
from flask import Flask

def create_app():
    load_dotenv()  # legge il .env

    app = Flask(__name__)

    app.secret_key = os.environ.get("FLASK_SECRET_KEY")

    # Route Login
    from web_app.routes.login import bp as login_bp
    app.register_blueprint(login_bp)

    # Route Home
    from web_app.routes.home import bp as main_bp
    app.register_blueprint(main_bp)

    # Route new Events
    from web_app.routes.new_events import bp as new_events
    app.register_blueprint(new_events)

    # Route get Events
    from web_app.routes.get_events import bp as get_events
    app.register_blueprint(get_events)

    # Route edit Events
    from web_app.routes.edit_events import bp as edit_events
    app.register_blueprint(edit_events)

    # Route Graph
    from web_app.routes.graph import bp as graph
    app.register_blueprint(graph)

    # Error Handlers
    from web_app.routes import error_page
    error_page.register_error_handlers(app)

    return app
