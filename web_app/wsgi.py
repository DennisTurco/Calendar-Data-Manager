"""WSGI entrypoint for production hosts (Vercel via pyproject.toml, or e.g. `gunicorn web_app.wsgi:app`)."""
import html
import logging
import traceback

try:
    from web_app import create_app

    app = create_app()
except Exception as exc:  # pragma: no cover - only hit when the deployment itself is broken
    # Keep the function alive so the cause is visible in the browser and in the host's logs,
    # instead of an opaque FUNCTION_INVOCATION_FAILED.
    logging.getLogger(__name__).error("App failed to start:\n%s", traceback.format_exc())
    from flask import Flask

    app = Flask(__name__)
    _reason = html.escape(f"{type(exc).__name__}: {exc}")

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def startup_failed(path):
        return (
            "<!doctype html><meta charset='utf-8'><title>Startup failed</title>"
            "<body style='font-family:system-ui;max-width:40rem;margin:4rem auto;padding:0 1rem'>"
            "<h1>The app failed to start</h1><p>Check the function logs for the full traceback.</p>"
            f"<pre style='white-space:pre-wrap;background:#f3f4f6;padding:1rem;border-radius:8px'>{_reason}</pre>",
            500,
        )
