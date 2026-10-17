#!/usr/bin/env bash
# Create a Seedance 2.0 clip with the KreatorFlow API, then wait for it.
# Needs: curl, jq, and KREATORFLOW_API_KEY in the environment.
set -euo pipefail
API=https://kreatorflow.ai/v1
AUTH="Authorization: Bearer ${KREATORFLOW_API_KEY:?set KREATORFLOW_API_KEY}"

JOB_ID=$(curl -sS "$API/videos" -H "$AUTH" -H "Content-Type: application/json" \
  -H "Idempotency-Key: example-$(date +%s)" \
  -d '{
    "model": "kreator-video-pro",
    "prompt": "slow dolly in on a glass perfume bottle on wet black stone, soft studio light, light rain",
    "duration": 5,
    "aspect_ratio": "16:9",
    "resolution": "720p"
  }' | jq -r '.data.job.id')
echo "job $JOB_ID"

while true; do
  JOB=$(curl -sS "$API/jobs/$JOB_ID" -H "$AUTH")
  STATUS=$(echo "$JOB" | jq -r '.data.job.status')
  case "$STATUS" in completed|failed|canceled|blocked) break ;; esac
  sleep 3
done
echo "$STATUS $(echo "$JOB" | jq -r '.data.job.providerOutputUrl')"
