# Websocket Validation

## Implementation

- Websocket URL construction is centralized in `frontend/src/services/socketClient.js`.
- The websocket base URL is read from `VITE_WS_URL`.
- If `VITE_WS_URL` is not supplied, the socket URL is inferred from `VITE_API_URL`.
- Secure production origins infer a secure websocket protocol.

## Stream Endpoint

- Atmospheric stream path: `/stream/atmospheric`
- Components should use `createAtmosphericSocket()`.

## Validation Status

- App websocket creation no longer contains hardcoded backend origins.
- Production bundle loopback scan returned zero matches.
- Reconnect/backoff behavior remains in `App.jsx`.
