import sys
import threading
import time
import urllib.error
import urllib.request
from pathlib import Path

import uvicorn

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

import main


ENDPOINTS = [
    "/",
    "/history",
    "/forecast",
    "/cwc/historical-dates",
    "/cwc/historical-observations",
    "/cwc/cape-traceability",
    "/cwc/latest-file-analyzed",
]

config = uvicorn.Config(
    main.app,
    host="127.0.0.1",
    port=8031,
    log_level="error",
    lifespan="off",
)
server = uvicorn.Server(config)
thread = threading.Thread(target=server.run, daemon=True)
thread.start()

base_url = "http://127.0.0.1:8031"
try:
    for _ in range(60):
        try:
            urllib.request.urlopen(f"{base_url}/", timeout=1).read()
            break
        except Exception:
            time.sleep(0.25)
    else:
        raise SystemExit("Server did not become ready")

    for endpoint in ENDPOINTS:
        with urllib.request.urlopen(f"{base_url}{endpoint}", timeout=30) as response:
            body = response.read()
            print(f"{endpoint} {response.status} {len(body)}")
            if response.status != 200:
                raise SystemExit(1)
except urllib.error.HTTPError as exc:
    print(f"HTTP_ERROR {exc.code} {exc.url}")
    raise SystemExit(1)
finally:
    server.should_exit = True
    thread.join(timeout=5)
