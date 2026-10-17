# Seedance API (Seedance 2.5, 2.0, Fast, Mini): Python, Node and curl examples

Generate ByteDance **Seedance** videos from your own code with the [KreatorFlow API](https://kreatorflow.ai/seedance-api). One API key covers Seedance 2.5, Seedance 2.0, Seedance 2.0 Fast and Seedance 2.0 Mini, plus Seedream images and text to speech. You pay per second of video from prepaid tokens, with no subscription.

KreatorFlow is an official partner of BytePlus, a ByteDance company.

- **Get a key:** [developers.kreatorflow.ai](https://developers.kreatorflow.ai/?section=keys)
- **Docs:** [developers.kreatorflow.ai/?section=docs](https://developers.kreatorflow.ai/?section=docs)
- **Prices and code for each model:** [kreatorflow.ai/seedance-api](https://kreatorflow.ai/seedance-api)

## Quickstart

```bash
export KREATORFLOW_API_KEY=your_api_key

# curl
./examples/curl/generate-video.sh

# Python (pip install requests)
python examples/python/generate_video.py

# Node 18+
node examples/node/generate-video.mjs
```

Each example creates a 5 second Seedance 2.0 clip at 720p, waits for it, then prints the download link. To switch models, change the `model` field:

| Model | `model` | Max length | Price per second at 720p | Model page |
| --- | --- | --- | --- | --- |
| Seedance 2.5 | `kreator-video-seedance-2-5` | 30 s | $0.207 | [Seedance 2.5 API](https://kreatorflow.ai/seedance-api/seedance-2-5) |
| Seedance 2.0 | `kreator-video-pro` | 15 s | $0.110 | [Seedance 2.0 API](https://kreatorflow.ai/seedance-api/seedance-2) |
| Seedance 2.0 Fast | `kreator-video-fast` | 10 s | $0.084 | [Seedance 2.0 Fast API](https://kreatorflow.ai/seedance-api/seedance-2-fast) |
| Seedance 2.0 Mini | `kreator-video-mini` | 10 s | $0.067 | [Seedance 2.0 Mini API](https://kreatorflow.ai/seedance-api/seedance-2-mini) |

## Seedance API pricing

Prices per second and per clip, with text or image input. They come from the KreatorFlow rate card on 17 October 2026. One token costs $0.05. The [price calculator](https://kreatorflow.ai/seedance-api) always shows current prices.

| Model | 480p | 720p | 1080p | 4K | Max length |
| --- | --- | --- | --- | --- | --- |
| Seedance 2.5 | $0.143/s | $0.207/s | $0.444/s | $0.999/s | 30 s |
| Seedance 2.0 | $0.076/s | $0.110/s | $0.240/s | $0.580/s | 15 s |
| Seedance 2.0 Fast | $0.058/s | $0.084/s | $0.183/s | n/a | 10 s |
| Seedance 2.0 Mini | $0.058/s | $0.067/s | $0.135/s | n/a | 10 s |

| One 5 second clip | 480p | 720p | 1080p | 4K |
| --- | --- | --- | --- | --- |
| Seedance 2.5 | $0.75 | $1.05 | $2.25 | $5.00 |
| Seedance 2.0 | $0.40 | $0.55 | $1.20 | $2.90 |
| Seedance 2.0 Fast | $0.30 | $0.45 | $0.95 | n/a |
| Seedance 2.0 Mini | $0.30 | $0.35 | $0.70 | n/a |

There's no subscription. Top-ups start at $20. A job that fails, is declined or times out costs nothing, because its reserved tokens go back to your balance. For a provider-by-provider comparison, with every price sourced and dated, see the [Seedance API price comparison](https://kreatorflow.ai/seedance-api-comparison).

## Examples in this repository

| File | What it does |
| --- | --- |
| [`examples/curl/generate-video.sh`](examples/curl/generate-video.sh) | Text to video with curl and jq |
| [`examples/python/generate_video.py`](examples/python/generate_video.py) | Text to video in Python, waits, saves the MP4 |
| [`examples/python/image_to_video.py`](examples/python/image_to_video.py) | Uploads a local image and animates it from the first frame at 1080p |
| [`examples/python/webhook_server.py`](examples/python/webhook_server.py) | Receives signed job webhooks (standard library only) |
| [`examples/node/generate-video.mjs`](examples/node/generate-video.mjs) | Text to video in Node 18+ |
| [`examples/node/batch-variants.mjs`](examples/node/batch-variants.mjs) | Renders several cheap Seedance 2.0 Fast variants of one idea |

Copy `.env.example` to `.env`, or export the variables in your shell.

## How a job works

1. `POST https://kreatorflow.ai/v1/videos` with `model`, `prompt`, `duration`, `aspect_ratio` and `resolution`. Add an `Idempotency-Key` header so a resent request doesn't create a second job.
2. The response holds `data.job.id`, `quoted_token_cost` and `balance_tokens`. Poll `GET /v1/jobs/{id}` until `status` is `completed`, `failed`, `canceled` or `blocked`. You can also pass `webhook_url` to get a signed callback instead.
3. Download `providerOutputUrl` with the same key and keep your own copy, because the link expires.

## Request fields

| Field | Description |
| --- | --- |
| `model` | `kreator-video-seedance-2-5`, `kreator-video-pro` (Seedance 2.0), `kreator-video-fast` or `kreator-video-mini` |
| `prompt` | Required. Subject, action, camera move, light and style |
| `duration` | Seconds, from the model's allowed lengths (`GET /v1/models`) |
| `resolution` | `480p`, `720p`, `1080p` or `4k`, where the model offers it |
| `aspect_ratio` | `16:9`, `9:16`, `1:1`, `4:3`, `3:4`, `21:9` or `adaptive` |
| `generate_audio` | Generate sound with the clip on models that support it |
| `seed` | Fix the seed to compare prompt wording |
| `first_frame_url` / `first_frame_upload_id` | Image the clip starts on |
| `last_frame_url` / `last_frame_upload_id` | Image the clip ends on |
| `reference_image_urls` / `reference_image_upload_ids` | Images that guide the look |
| `reference_video_urls` / `reference_video_upload_ids` | Clips that guide motion. Input seconds are billed at 60% of the rate |
| `reference_audio_urls` / `reference_audio_upload_ids` | Audio that guides voice or music |
| `webhook_url` | HTTPS URL that gets a signed event when the job ends |

The full reference, covering the job object, webhook signatures, uploads, rate limits and every error code, is at [kreatorflow.ai/seedance-api/reference](https://kreatorflow.ai/seedance-api/reference).

## Writing Seedance prompts

- Lead with the subject and the action. Then give the camera move, then the light and style.
- Use camera language: dolly in, crane down, orbit, tracking shot, handheld, locked-off.
- For image to video, describe only what moves. The image already sets the look.
- On Seedance 2.5, write long shots as a timeline: "0 to 10 s: …, 10 to 20 s: …".
- Draft on Fast or Mini at 480p with a fixed `seed`, then render the keeper on Seedance 2.0 or 2.5 at 1080p.

**Weak prompt:** `a city at night, cool`

**Strong prompt:** `Aerial flythrough of a futuristic neon city at night, flying between towers covered in glowing signs, rain-slick streets reflecting blue and magenta light, light fog, smooth fast drone move, filmic color grade.`

More tips: [Seedance prompt guide](https://kreatorflow.ai/guides/seedance-2-prompt-guide).

## Common errors

| Code | Meaning | Fix |
| --- | --- | --- |
| `invalid_api_key` (401) | Missing, wrong or revoked key | Send `Authorization: Bearer <key>` |
| `insufficient_balance` (402) | Balance below the job's quote | Top up in the console. Nothing was reserved |
| `duration_not_supported` (400) | The model doesn't offer that length | Use one of the model's durations |
| `rate_limited` (429) | Too many requests | Wait the seconds in `Retry-After` |
| `reference_rejected` (job) | A reference was declined, often a real person's photo | Register an owned character, or use another image |
| `generation_rejected` (job) | The prompt or options were declined | Change them and create a new job |

Every code is explained in [Seedance API errors](https://kreatorflow.ai/guides/seedance-api-errors).

## FAQ

**How do I get a Seedance API key?** Sign in at [developers.kreatorflow.ai](https://developers.kreatorflow.ai/?section=keys), create a key and top up from $20. There's no waitlist and no contract. See [How to get a Seedance API key](https://kreatorflow.ai/guides/how-to-get-a-seedance-api-key).

**Is there a free Seedance API?** No provider offers a free production Seedance 2.0 or 2.5 API. On KreatorFlow you pay per second, and failed jobs cost nothing. See [Is there a free Seedance API?](https://kreatorflow.ai/guides/is-there-a-free-seedance-api).

**Which Seedance model should I use?** Use Mini or Fast for drafts, Seedance 2.0 for cinematic shots up to 4K, and Seedance 2.5 for single takes up to 30 seconds. See [Seedance API tiers compared](https://kreatorflow.ai/guides/seedance-api-models-compared).

**What are the rate limits?** 20 video jobs a minute and 120 job polls a minute per developer account. See [Seedance API rate limits](https://kreatorflow.ai/guides/seedance-api-rate-limits).

**Can I use it from Claude or ChatGPT?** Yes, through the [KreatorFlow MCP server](https://kreatorflow.ai/mcp).

## More

- [Seedance API quickstart guide](https://kreatorflow.ai/guides/seedance-api-quickstart)
- [AI video API webhooks](https://kreatorflow.ai/guides/ai-video-api-webhooks)
- [KreatorFlow API blog](https://kreatorflow.ai/blog/api)

MIT licensed. Seedance and Seedream are ByteDance models. KreatorFlow is an official partner of BytePlus, a ByteDance company. This repository holds example code for the KreatorFlow API.
