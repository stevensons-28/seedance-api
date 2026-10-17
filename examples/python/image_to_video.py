"""Animate a local image with Seedance 2.0 on the KreatorFlow API.

Uploads the image (POST /v1/uploads, PUT the bytes, POST /v1/uploads/complete), then uses it as the
first frame of a 5 second clip.

pip install requests
export KREATORFLOW_API_KEY=your_api_key
python image_to_video.py path/to/photo.png "the camera slowly pushes in as the wind moves her hair"
"""
import mimetypes
import os
import sys
import time
import uuid

import requests

API = "https://kreatorflow.ai/v1"
AUTH = {"Authorization": f"Bearer {os.environ['KREATORFLOW_API_KEY']}"}


def upload(path: str) -> str:
    mime = mimetypes.guess_type(path)[0] or "image/png"
    data = open(path, "rb").read()
    created = requests.post(
        f"{API}/uploads",
        headers=AUTH,
        json={"file_name": os.path.basename(path), "mime_type": mime, "file_size": len(data), "upload_type": "IMAGE"},
        timeout=60,
    ).json()["data"]
    # PUT the bytes with exactly the headers we were given (the Content-Type is signed).
    requests.put(created["direct_upload_url"], headers=created["direct_upload_headers"], data=data, timeout=300).raise_for_status()
    requests.post(f"{API}/uploads/complete", headers=AUTH, json={"upload_id": created["upload_id"]}, timeout=60).raise_for_status()
    return created["upload_id"]


def main() -> None:
    image, prompt = sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "slow push in, soft natural motion"
    upload_id = upload(image)
    job = requests.post(
        f"{API}/videos",
        headers={**AUTH, "Idempotency-Key": str(uuid.uuid4())},
        json={
            "model": "kreator-video-pro",
            "prompt": prompt,
            "first_frame_upload_id": upload_id,
            "duration": 5,
            "aspect_ratio": "adaptive",
            "resolution": "1080p",
        },
        timeout=60,
    ).json()["data"]["job"]
    while job["status"] not in ("completed", "failed", "canceled", "blocked"):
        time.sleep(10)
        job = requests.get(f"{API}/jobs/{job['id']}", headers=AUTH, timeout=60).json()["data"]["job"]
    if job["status"] != "completed":
        raise SystemExit(f"job {job['status']}: {job.get('errorCode')}")
    with open("image-to-video.mp4", "wb") as file:
        file.write(requests.get(job["providerOutputUrl"], headers=AUTH, timeout=300).content)
    print("saved image-to-video.mp4")


if __name__ == "__main__":
    main()
