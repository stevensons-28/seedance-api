// Create a Seedance 2.0 clip with the KreatorFlow API, wait for it and save it.
// Node 18+:  KREATORFLOW_API_KEY=your_api_key node generate-video.mjs
import { randomUUID } from "node:crypto";
import { writeFile } from "node:fs/promises";

const API = "https://kreatorflow.ai/v1";
const headers = { Authorization: `Bearer ${process.env.KREATORFLOW_API_KEY}` };

let { data } = await fetch(`${API}/videos`, {
  method: "POST",
  headers: { ...headers, "Content-Type": "application/json", "Idempotency-Key": randomUUID() },
  body: JSON.stringify({
    model: "kreator-video-pro", // or kreator-video-seedance-2-5, kreator-video-fast, kreator-video-mini
    prompt: "slow dolly in on a glass perfume bottle on wet black stone, soft studio light, light rain",
    duration: 5,
    aspect_ratio: "16:9",
    resolution: "720p",
  }),
}).then((response) => response.json());

let job = data.job;
console.log("job", job.id);
while (!["completed", "failed", "canceled", "blocked"].includes(job.status)) {
  await new Promise((resolve) => setTimeout(resolve, 3000));
  ({ data } = await fetch(`${API}/jobs/${job.id}`, { headers }).then((response) => response.json()));
  job = data.job;
}
if (job.status !== "completed") throw new Error(`job ${job.status}: ${job.errorCode ?? ""}`);

// The output link needs the same key and expires, so keep your own copy.
const video = await fetch(job.providerOutputUrl, { headers });
await writeFile("seedance.mp4", Buffer.from(await video.arrayBuffer()));
console.log("saved seedance.mp4");
