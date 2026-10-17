# Seedance API: Seedance 2.5, 2.0, Fast and Mini from one key

Generate ByteDance **Seedance** videos from your own code with the [KreatorFlow API](https://kreatorflow.ai/seedance-api). One API key covers Seedance 2.5, Seedance 2.0, Seedance 2.0 Fast and Seedance 2.0 Mini, plus Seedream images and text to speech. You pay per second of video from prepaid tokens, with no subscription.

KreatorFlow is an official BytePlus partner. It's built on BytePlus, ByteDance's official AI platform.

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

Prices per 5 second clip, with text or image input, from the KreatorFlow rate card on 17 October 2026. One token costs $0.05.

| Resolution | Seedance 2.5 | Seedance 2.0 | Seedance 2.0 Fast | Seedance 2.0 Mini |
| --- | --- | --- | --- | --- |
| 480p | $0.75 | $0.40 | $0.30 | $0.30 |
| 720p | $1.05 | $0.55 | $0.45 | $0.35 |
| 1080p | $2.25 | $1.20 | $0.95 | $0.70 |
| 4K | $5.00 | $2.90 | n/a | n/a |

Current prices for every resolution and length are on each model page. For a provider-by-provider comparison, with every price sourced and dated, see the [Seedance API price comparison](https://kreatorflow.ai/seedance-api-comparison).

## How a job works

1. `POST https://kreatorflow.ai/v1/videos` with `model`, `prompt`, `duration`, `aspect_ratio` and `resolution`. Add an `Idempotency-Key` header so a resent request doesn't create a second job.
2. The response holds `data.job.id`. Poll `GET /v1/jobs/{id}` until `status` is `completed`, `failed`, `canceled` or `blocked`. You can also pass `webhook_url` to get a signed callback instead.
3. Download `providerOutputUrl` with the same key and keep your own copy.

References (images, video clips, audio) go in as upload ids from `POST /v1/uploads` or as public HTTPS URLs. `GET /v1/models` lists every model with its durations, resolutions and reference limits.

## More

- [Seedance API quickstart guide](https://kreatorflow.ai/guides/seedance-api-quickstart)
- [AI video API webhooks](https://kreatorflow.ai/guides/ai-video-api-webhooks)
- [KreatorFlow API blog](https://kreatorflow.ai/blog/api)
- [MCP server for Claude and ChatGPT](https://kreatorflow.ai/mcp)

MIT licensed. Seedance and Seedream are ByteDance models. This repository holds example code for the KreatorFlow API.
