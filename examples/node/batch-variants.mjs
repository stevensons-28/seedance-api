// Render several cheap Seedance 2.0 Fast variants of one idea, then pick the best.
// Each variant gets its own Idempotency-Key, so a resent request never creates a second job.
// Node 18+:  KREATORFLOW_API_KEY=your_api_key node batch-variants.mjs
import { randomUUID } from "node:crypto";

const API = "https://kreatorflow.ai/v1";
const headers = { Authorization: `Bearer ${process.env.KREATORFLOW_API_KEY}` };
const base = "A white sneaker spins slowly on a concrete plinth, hard side light, dust in the air";
const cameras = ["camera slowly orbits right", "slow push in", "locked-off camera, low angle"];

const jobs = await Promise.all(
  cameras.map(async (camera) => {
    const { data } = await fetch(`${API}/videos`, {
      method: "POST",
      headers: { ...headers, "Content-Type": "application/json", "Idempotency-Key": randomUUID() },
      body: JSON.stringify({ model: "kreator-video-fast", prompt: `${base}, ${camera}`, duration: 5, aspect_ratio: "9:16", resolution: "720p" }),
    }).then((response) => response.json());
    return data.job;
  }),
);

for (let job of jobs) {
  while (!["completed", "failed", "canceled", "blocked"].includes(job.status)) {
    await new Promise((resolve) => setTimeout(resolve, 10000));
    job = (await fetch(`${API}/jobs/${job.id}`, { headers }).then((response) => response.json())).data.job;
  }
  console.log(job.id, job.status, job.providerOutputUrl ?? job.errorCode);
}
