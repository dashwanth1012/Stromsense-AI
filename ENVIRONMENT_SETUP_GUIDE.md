# Environment Setup Guide

## Frontend: Vercel

Set:

- `VITE_API_URL`
- `VITE_WS_URL`
- `VITE_APP_ENV=production`

Then rebuild/redeploy the frontend.

## Backend: Railway Or Equivalent

Set:

- `DATABASE_URL`
- `JWT_SECRET`
- `CORS_ALLOW_ORIGINS`
- `CORS_ALLOW_ORIGIN_REGEX` if needed

For `CORS_ALLOW_ORIGINS`, include the deployed Vercel origin and any approved custom domains.

## Local Development

Use `frontend/.env.development` for local workstation API routing. Do not commit secrets into frontend environment files.

## Production Safety Rule

The frontend must not store database credentials, service-role keys, or backend secrets. Only public API routing variables belong in the frontend environment.
