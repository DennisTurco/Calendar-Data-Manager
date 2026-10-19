"""WSGI entrypoint for production hosts (Vercel via pyproject.toml, or e.g. `gunicorn web_app.wsgi:app`)."""
from web_app import create_app

app = create_app()
