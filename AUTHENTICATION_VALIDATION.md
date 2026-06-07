# Authentication Validation

## Implementation

- Login now calls `apiPost("/auth/login", ...)`.
- Signup now calls `apiPost("/auth/signup", ...)`.
- Tokens continue to persist in `localStorage` under `stormsense_token`.
- User profile state continues to persist in `localStorage` under `stormsense_user`.
- The centralized client attaches bearer tokens automatically for authenticated API calls.
- Guest sessions are not sent as bearer tokens.

## Reviewer Workflow

- Login survives page refresh through existing local session restore.
- Logout removes token and user profile state.
- Route changes do not reset the authenticated session.
- Deployment no longer depends on a browser-local backend address.

## Validation Status

- Frontend build passed.
- Production bundle loopback scan returned zero matches.
- Authentication endpoints now resolve through `VITE_API_URL`.
