import asyncio

import websockets


async def main():
    for port in (8010, 8000, 8002, 8001, 8004):
        for path in ("/stream/atmospheric", "/stream/atmospheric/"):
            try:
                async with websockets.connect(f"ws://127.0.0.1:{port}{path}") as ws:
                    message = await asyncio.wait_for(ws.recv(), timeout=8)
                    print("WEBSOCKET_OK", port, path, len(message))
                    return
            except Exception as exc:
                print("WEBSOCKET_FAIL", port, path, type(exc).__name__)
    raise SystemExit(1)


asyncio.run(main())
