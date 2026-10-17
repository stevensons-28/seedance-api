"""Create a Seedance 2.0 clip with the KreatorFlow API, wait for it and save it.

pip install requests
export KREATORFLOW_API_KEY=your_api_key
python generate_video.py
"""
import os
import time
import uuid

import requests

API = "https://kreatorflow.ai/v1"
HEADERS = {"Authorization": f"Bearer {os.environ['KREATORFLOW_API_KEY']}"}

job = requests.post(
    f"{API}/videos",
    headers={**HEADERS, "Idempotency-Key": str(uuid.uuid4())},
    json={
        "model": "kreator-video-pro",  # or kreator-video-seedance-2-5, kreator-video-fast, kreator-video-mini
        "prompt": "slow dolly in on a glass perfume bottle on wet black stone, soft studio light, light rain",
        "duration": 5,
        "aspect_ratio": "16:9",
        "resolution": "720p",
    },
    timeout=60,
).json()["data"]["job"]
print("job", job["id"])

while job["status"] not in ("completed", "failed", "canceled", "blocked"):
    time.sleep(3)
    job = requests.get(f"{API}/jobs/{job['id']}", headers=HEADERS, timeout=60).json()["data"]["job"]

if job["status"] != "completed":
    raise SystemExit(f"job {job['status']}: {job.get('errorCode')}")

# The output link needs the same key and expires, so keep your own copy.
video = requests.get(job["providerOutputUrl"], headers=HEADERS, timeout=300)
with open("seedance.mp4", "wb") as file:
    file.write(video.content)
print("saved seedance.mp4")
