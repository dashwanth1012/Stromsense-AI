# StormSense AI Deployment Guide

## Target Deployment
StormSense AI is configured for a single Render Web Service serving both FastAPI APIs and the Vite React frontend from one URL.

## Render Build Process
```text
python -m pip install --upgrade pip
pip install -r backend/requirements.txt
cd frontend && npm install && npm run build
```

## Render Start Command
```text
uvicorn backend.main:app --host 0.0.0.0 --port $PORT
```

## Environment Variables
| Variable | Purpose |
| --- | --- |
| DATABASE_URL | Supabase PostgreSQL connection string with SSL mode. |
| SUPABASE_URL | Supabase project API URL. |
| SUPABASE_ANON_KEY | Client-safe Supabase key where needed. |
| SUPABASE_SERVICE_ROLE_KEY | Server-side Supabase service key; never expose in frontend. |
| JWT_SECRET | Authentication signing secret. |
| CORS_ALLOW_ORIGINS | Optional comma-separated CORS allow-list. |

## Static Frontend Serving
FastAPI serves `frontend/dist/assets` at `/assets` and returns `frontend/dist/index.html` for browser navigation routes.

## API Preservation
Backend prefixes `/auth`, `/cwc`, `/history`, `/system-status`, `/stream`, `/trend-analysis`, and `/storm-escalation` are protected from SPA fallback.

## Troubleshooting
- If the Render URL returns backend JSON at `/`, confirm the frontend build exists before startup.
- If `/forecast` opens JSON in a browser, confirm the browser sends `Accept: text/html`; API calls use `Accept: application/json`.
- If uploads fail, verify `python-multipart`, `openpyxl`, and `xlrd` are installed from requirements.
- If database writes fail, verify `DATABASE_URL` and Supabase network access.
