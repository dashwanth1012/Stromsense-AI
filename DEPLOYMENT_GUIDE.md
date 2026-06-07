# StormSense AI Supabase Deployment Guide

## 1. Supabase

1. Create a Supabase project.
2. Open SQL Editor.
3. Run `supabase_schema.sql`.
4. Confirm these storage buckets exist:
   - `historical-archives`
   - `uploaded-soundings`
   - `review-exports`
   - `forecast-exports`
   - `bulletins`
5. Copy the Supabase PostgreSQL connection string.

## 2. Data Migration

Install backend requirements, then run:

```powershell
cd "C:\Users\USER\Thunderstorm analysis"
$env:DATABASE_URL="postgresql://..."
backend\venv\Scripts\python.exe migration_runner.py --apply
```

Dry-run without writing:

```powershell
backend\venv\Scripts\python.exe migration_runner.py
```

Expected source counts:

- `users`: 3
- `thunderstorm_forecasts`: 942

## 3. Railway Backend

Set environment variables:

```text
DATABASE_URL=
SUPABASE_URL=
SUPABASE_ANON_KEY=
SUPABASE_SERVICE_ROLE_KEY=
JWT_SECRET=
```

Install command:

```text
pip install -r backend/requirements.txt
```

Start command:

```text
cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT
```

## 4. Vercel Frontend

Build command:

```text
cd frontend && npm install && npm run build
```

Output directory:

```text
frontend/dist
```

Configure frontend API base URL to the Railway backend URL if deployment introduces a non-local API host.

## 5. Deployment Validation

Required smoke checks:

- `/`
- `/forecast`
- `/history`
- `/cwc/historical-dates`
- `/cwc/historical-observations`
- `/cwc/cape-traceability`
- `/cwc/latest-file-analyzed`
- `/system-status`
- `/stream/atmospheric`

## 6. Rollback

The migration is additive at the code level. If Supabase is unavailable, unset `DATABASE_URL` to keep non-persistent forecast/archive workflows running while persistence is repaired.
