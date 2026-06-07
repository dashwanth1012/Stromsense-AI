import json
import sys
import threading
import time
import urllib.request
import uuid
from pathlib import Path

import uvicorn

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

import main


sample_path = ROOT / "scratch" / "sample_historical_upload.csv"
file_bytes = sample_path.read_bytes()
boundary = f"----StormSenseBoundary{uuid.uuid4().hex}"
body = b"".join(
    [
        f"--{boundary}\r\n".encode(),
        b'Content-Disposition: form-data; name="file"; filename="sample_historical_upload.csv"\r\n',
        b"Content-Type: text/csv\r\n\r\n",
        file_bytes,
        f"\r\n--{boundary}--\r\n".encode(),
    ]
)

config = uvicorn.Config(
    main.app,
    host="127.0.0.1",
    port=8033,
    log_level="error",
    lifespan="off",
)
server = uvicorn.Server(config)
thread = threading.Thread(target=server.run, daemon=True)
thread.start()

base_url = "http://127.0.0.1:8033"
try:
    for _ in range(60):
        try:
            urllib.request.urlopen(f"{base_url}/", timeout=1).read()
            break
        except Exception:
            time.sleep(0.25)
    else:
        raise SystemExit("Server did not become ready")

    request = urllib.request.Request(
        f"{base_url}/cwc/analyze-historical-dataset",
        data=body,
        method="POST",
        headers={
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Content-Length": str(len(body)),
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        payload = json.loads(response.read().decode("utf-8"))
        analysis = payload["analysis"]
        print("UPLOAD_STATUS", response.status)
        print("TOTAL_RECORDS", analysis["total_records"])
        print("THUNDERSTORM_RECORDS", analysis["thunderstorm_records"])
        print("QUALITY_SCORE", analysis["quality_score"])
        if response.status != 200 or analysis["total_records"] <= 0:
            raise SystemExit(1)
finally:
    server.should_exit = True
    thread.join(timeout=5)
