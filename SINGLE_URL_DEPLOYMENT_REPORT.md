# StormSense AI Single-URL Render Deployment Report

Generated: 2026-06-08

## Objective

Serve the existing StormSense AI Vite frontend and FastAPI backend from one Render Web Service and one public URL.

No UI redesign, scientific logic changes, forecast logic changes, CAPE logic changes, probability logic changes, research logic changes, or database logic changes were made.

## Project Structure

| Area | Path | Status |
|---|---|---|
| Backend package | `backend/` | Operational FastAPI app |
| Frontend source | `frontend/` | Vite React app |
| Frontend build output | `frontend/dist` | Built successfully |
| Existing requirements file | `backend/requirements.txt` | Preserved |
| Single Render blueprint | `render.yaml` | Added one web service only |

## Frontend Build Validation

Commands run:

```text
cd frontend
npm install
npm run build
```

Result:

- `npm install`: passed, dependencies up to date.
- `npm run build`: passed.
- Build output: `frontend/dist/index.html`
- Static assets: `frontend/dist/assets/`

## FastAPI Static Configuration

`backend/main.py` now resolves:

- Project root: parent directory of `backend/`
- Frontend dist path: `frontend/dist`
- Frontend index file: `frontend/dist/index.html`
- Frontend asset path: `frontend/dist/assets`

FastAPI mounts:

```text
/assets -> frontend/dist/assets
```

Browser navigation requests that accept `text/html` are served with `frontend/dist/index.html`.

## SPA Routing Configuration

The SPA fallback is registered after existing backend routes.

Validated frontend/browser routes:

| Route | Expected | Result |
|---|---|---|
| `/` with `Accept: text/html` | React app shell | 200 HTML |
| `/dashboard` | React app shell | 200 HTML |
| `/research` | React app shell | 200 HTML |
| `/archive` | React app shell | 200 HTML |
| `/forecast` with `Accept: text/html` | React app shell | 200 HTML |

The `/forecast` conflict is handled by request type:

- Browser navigation with `Accept: text/html` receives the React shell.
- API calls with `Accept: application/json` receive the forecast JSON payload.

## API Routing Validation

Validated API routes:

| Route | Expected | Result |
|---|---|---|
| `/` with `Accept: application/json` | Backend status JSON | 200 JSON |
| `/system-status` | System status JSON | 200 JSON |
| `/history` | Forecast history JSON | 200 JSON |
| `/cwc/historical-dates` | Historical archive dates JSON | 200 JSON |
| `/forecast` with `Accept: application/json` | Forecast JSON array | 200 JSON, 60,509 bytes |

Reserved backend prefixes remain protected from SPA fallback:

```text
/auth
/cwc
/docs
/openapi.json
/redoc
/history
/system-status
/stream
/storm-escalation
/trend-analysis
```

## Frontend API Configuration

Production frontend API and websocket resolution uses the deployed origin.

- `frontend/src/config/environment.js` already resolves production API calls from `window.location.origin`.
- `frontend/src/config/environment.js` derives websocket origin from the same deployed origin.
- `frontend/.env.production` remains blank for `VITE_API_URL` and `VITE_WS_URL`, allowing same-origin production behavior.
- `frontend/.env.development` no longer hardcodes `localhost`.

Source scan result:

- No active frontend source or env file contains `localhost` or `127.0.0.1`.
- Remaining local references are limited to old reports and scratch validation scripts.

## Render Deployment Configuration

`render.yaml` defines a single web service:

```text
type: web
env: python
buildCommand:
  python -m pip install --upgrade pip
  pip install -r backend/requirements.txt
  cd frontend && npm install && npm run build
startCommand:
  uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

No second Render service, static site, Vercel deployment, or separate frontend deployment is required.

Required Render environment variables remain service-level secrets:

- `DATABASE_URL`
- `SUPABASE_URL`
- `SUPABASE_ANON_KEY`
- `SUPABASE_SERVICE_ROLE_KEY`
- `JWT_SECRET`

## Backend Validation

Commands run:

```text
python -m py_compile backend/main.py
python -c "import backend.main; print('IMPORT_OK')"
uvicorn backend.main:app
```

Results:

- `py_compile`: passed.
- `import backend.main`: passed.
- Uvicorn startup: passed.
- Application startup: complete.

Local route validation used alternate ports because local port `8000` was already occupied. Render uses `$PORT`, so this does not affect deployment.

## Final Status

Single-URL Render deployment wiring is ready.

The Render service URL should now:

- Load the StormSense AI frontend for browser visits.
- Preserve existing backend APIs.
- Preserve websocket route registration.
- Support SPA refreshes for operational frontend routes.
- Build frontend and backend inside one Render Web Service.
