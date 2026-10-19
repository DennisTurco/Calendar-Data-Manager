# Deploying the web app on Vercel

The web app (`web_app/`) runs on Vercel as a single Python function. The desktop app is not deployed.

## What the repository already provides

| File | Purpose |
|---|---|
| `pyproject.toml` | Web-only dependencies + `tool.vercel.entrypoint = "web_app.wsgi:app"` + build step |
| `web_app/wsgi.py` | Production entrypoint (`app = create_app()`) — also works with `gunicorn web_app.wsgi:app` |
| `scripts/vercel_build.py` | Copies `web_app/static` to `public/static` so Vercel serves CSS/JS/images from its CDN |
| `vercel.json` | Function timeout (60 s), files excluded from the bundle, long cache for `/static/*` |
| `.vercelignore` | Keeps the desktop app, the desktop `requirements.txt` and local tooling out of the deployment |

The app is **stateless**: no database or Redis is needed. After sign-in, the Google tokens are stored in the
user's session cookie, **encrypted** with a key derived from `FLASK_SECRET_KEY` (the OAuth client secret never
goes in the cookie). Charts are rendered directly in the search response, and bulk edits repeat the search at
confirm time, refusing to apply changes if the matched events changed since the preview.

If a required variable is missing (`FLASK_SECRET_KEY`, `GOOGLE_CLIENT_ID`, `GOOGLE_CLIENT_SECRET`, `GOOGLE_REDIRECT_URI`), every page shows a **"Setup incomplete"** screen listing the missing names (never their values). If the app crashes while starting, a **"The app failed to start"** page shows the error type and message; the full traceback is in the function logs (Vercel → Project → *Logs*).

## 1. Google Cloud Console (OAuth)

1. **APIs & Services → Credentials → Create credentials → OAuth client ID**, type **Web application**
   (or reuse the one you use locally).
2. **Authorized redirect URIs** — add the production URL:
   `https://<your-project>.vercel.app/login/callback`
   (and `https://<your-domain>/login/callback` if you add a custom domain).
   Google does not accept wildcards, so Vercel *preview* deployments (random URLs) cannot log in:
   test on the production domain, or on a fixed alias you also register here.
3. **OAuth consent screen**: the app uses the sensitive `calendar` scope.
   - In **Testing** mode only the *test users* you list (max 100) can sign in, and they must sign in again every 7 days.
   - To open it to anyone, publish the app and complete Google's verification (privacy policy, home page, scope justification video). Plan for days to weeks.
4. Make sure the **Google Calendar API** is enabled for the project.

## 2. Vercel project

1. **Add New → Project → import the GitHub repository**. Leave *Root Directory* as the repository root
   (the web app imports code from `common/`). Vercel detects Flask from `pyproject.toml`.
2. **Settings → Environment Variables** (Production):

   | Name | Value |
   |---|---|
   | `FLASK_SECRET_KEY` | a long random string, e.g. `python -c "import secrets; print(secrets.token_hex(32))"` |
   | `GOOGLE_CLIENT_ID` | from step 1 |
   | `GOOGLE_CLIENT_SECRET` | from step 1 |
   | `GOOGLE_REDIRECT_URI` | `https://<your-project>.vercel.app/login/callback` (exactly as registered) |

   Keep `FLASK_SECRET_KEY` stable: changing it signs everyone out (their encrypted tokens can no longer be read).

   Do **not** set `FLASK_ENV=development` in production: it enables plain-HTTP OAuth and shows error details.
3. Deploy. In the build log check that dependencies come from `pyproject.toml` and that
   `scripts/vercel_build.py` prints `Copied … -> public/static`.

## 3. Smoke test

1. Open `https://<your-project>.vercel.app/` → you should land on the sign-in page with styles loaded.
2. Sign in with a Google account listed as test user → you're back on Home with your name and photo.
3. Open *Get events*, pick *This month*, *Get list* → events appear. Reload the page: you should still be signed in
   (if you're sent back to login, check that `FLASK_SECRET_KEY` is set and that you use the HTTPS URL).

## Troubleshooting

| Symptom | Likely cause |
|---|---|
| "Setup incomplete" page | the listed environment variables are missing: add them and **redeploy** (variables apply only to new deployments) |
| `500 FUNCTION_INVOCATION_FAILED` | the function crashed before Flask could answer: open the deployment's *Logs* / *Runtime Logs* for the traceback |
| `redirect_uri_mismatch` from Google | `GOOGLE_REDIRECT_URI` differs from the URI registered in the Console (scheme, domain, trailing slash) |
| `InsecureTransportError` / `(insecure_transport) OAuth 2 MUST utilize https` | request reached Flask as HTTP; `ProxyFix` in `web_app/__init__.py` handles Vercel's headers — check you're on the HTTPS URL |
| Logged out on every page | `FLASK_SECRET_KEY` changed between deployments, or the site is opened over plain HTTP (secure cookie not sent) |
| `access_denied` / "app not verified" | account is not in the consent screen's test users, or the app isn't verified yet |
| Page without styles | `public/static` wasn't built: check the build step in the log |
| Function timeout on big ranges | the search spans many events; narrow the range or raise `maxDuration` in `vercel.json` (plan limits apply) |

## Updating styles

The compiled Tailwind CSS (`web_app/static/css/tailwind.css`) is committed, so Vercel needs no Node build.
After changing templates, rebuild it locally (`cd web_app && npm install && npm run build:css`) and commit the result.
