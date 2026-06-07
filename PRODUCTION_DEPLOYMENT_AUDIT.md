# Production Deployment Audit

## Scope

Phase 6.3 hardened the frontend/backend transport architecture without changing forecasting, CAPE, probability, verification, historical archive, or research algorithms.

## Changes Verified

- Frontend API routing now resolves through `frontend/src/config/environment.js`.
- Frontend requests now use `frontend/src/services/apiClient.js`.
- Websocket routing now uses `frontend/src/services/socketClient.js`.
- Authentication, forecast, history, archive, upload, verification, and research calls no longer choose backend URLs independently.
- Backend CORS now reads `CORS_ALLOW_ORIGINS` and `CORS_ALLOW_ORIGIN_REGEX`.

## Production Build Validation

- Command: `npm run build`
- Result: Passed
- Built output: `frontend/dist`
- Production bundle loopback scan: zero matches
- Frontend source production scan: zero matches

## Deployment Readiness

Set these variables in Vercel:

- `VITE_API_URL`
- `VITE_WS_URL`
- `VITE_APP_ENV=production`

Set these variables in Railway/backend hosting:

- `DATABASE_URL`
- `JWT_SECRET`
- `CORS_ALLOW_ORIGINS`
- `CORS_ALLOW_ORIGIN_REGEX` if wildcard domain matching is needed

Result: Ready for deployment testing once the production backend URL is assigned to the frontend environment.
