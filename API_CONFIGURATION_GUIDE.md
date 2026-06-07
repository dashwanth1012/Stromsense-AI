# API Configuration Guide

## Single Source Of Truth

Frontend API configuration lives in:

- `frontend/src/config/environment.js`
- `frontend/src/services/apiClient.js`
- `frontend/src/services/socketClient.js`

Components must not construct backend origins manually. They should use:

- `apiGet(path)`
- `apiPost(path, payload)`
- `apiUpload(path, formData)`
- `buildApiUrl(path)` for download links
- `createAtmosphericSocket()` for websocket streams

## Required Frontend Variables

- `VITE_API_URL`: deployed FastAPI backend origin
- `VITE_WS_URL`: deployed websocket origin
- `VITE_APP_ENV`: `development`, `staging`, or `production`

## Required Backend Variables

- `DATABASE_URL`: Supabase PostgreSQL URL
- `JWT_SECRET`: token signing secret
- `CORS_ALLOW_ORIGINS`: comma-separated frontend origins
- `CORS_ALLOW_ORIGIN_REGEX`: optional regex for future custom domains

## Deployment Rule

Future backend or frontend domain changes should be handled through environment variables only. No React component should require source modification for a deployment URL change.
