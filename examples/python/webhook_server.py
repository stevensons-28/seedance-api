"""A minimal webhook receiver for KreatorFlow job events (standard library only).

Pass webhook_url="https://your-host/kreatorflow" when you create a job. Each event is signed:
X-KreatorFlow-Signature: t=<unix seconds>,v1=<hex HMAC-SHA256 of "<t>.<raw body>">.

export KREATORFLOW_WEBHOOK_SECRET=your_webhook_secret
python webhook_server.py   # listens on :8080
"""
import hashlib
import hmac
import json
import os
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

SECRET = os.environ["KREATORFLOW_WEBHOOK_SECRET"]
seen: set[str] = set()


def verify_kreatorflow_webhook(raw_body: bytes, signature_header: str, secret: str) -> bool:
    parts = dict(part.split("=", 1) for part in signature_header.split(","))
    signed = f"{parts['t']}.".encode() + raw_body
    expected = hmac.new(secret.encode(), signed, hashlib.sha256).hexdigest()
    fresh = abs(time.time() - int(parts["t"])) < 300  # reject replays older than 5 min
    return fresh and hmac.compare_digest(expected, parts.get("v1", ""))


class Handler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:
        raw = self.rfile.read(int(self.headers.get("Content-Length", 0)))
        if not verify_kreatorflow_webhook(raw, self.headers.get("X-KreatorFlow-Signature", ""), SECRET):
            self.send_response(401)
            self.end_headers()
            return
        # Answer fast, then do the work. The event id lets you ignore an event you already handled.
        self.send_response(200)
        self.end_headers()
        event_id = self.headers.get("X-KreatorFlow-Event-Id", "")
        if event_id in seen:
            return
        seen.add(event_id)
        event = json.loads(raw)
        print(event.get("type"), json.dumps(event.get("data", {}))[:300])


if __name__ == "__main__":
    HTTPServer(("", 8080), Handler).serve_forever()
