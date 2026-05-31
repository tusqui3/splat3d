# splat3D

A hobby project for turning a short video into a 3D Gaussian Splat.

It takes a 5–10 sec video, does the AI / vision / neural pipeline, and gives you a splat viewer with a share link

---

## What it does

- upload a short video
- pull out frames
- figure out the camera / scene
- run the neural 3D reconstruction
- export a `.splat`
- open it in a viewer

Mostly built around vision, neural recon...

---

## How it runs

This can run in 2 ways:

- **local GPU**: best for the real reconstruction / training part
- **server**: also works if you run the worker on a CUDA box or some GPU server

The frontend can just run normal, but the worker really wants a GPU if you want the full 3D neural pipeline to happen.

---

## Tiny architecture

```text
browser
  ↓
frontend (Next.js / TypeScript / Tailwind)
  ↓
backend (FastAPI + SQLite)
  ↓
worker (Python)
  ↓
frames → colmap-ish stuff → 3DGS / neural recon → export splat
```

---

## Quick start

```bash
cp .env.example .env
docker compose up --build
```

Then open:

- frontend: `http://localhost:3000`
- backend: `http://localhost:8000`
- docs: `http://localhost:8000/docs`

---

## Local dev, no Docker

### backend

```bash
cd backend
pip install -r requirements.txt
DATA_DIR=/tmp/splat3d uvicorn main:app --reload --port 8000
```

### worker

```bash
cd worker
# ffmpeg needs to be installed
DATA_DIR=/tmp/splat3d python worker.py
```

### frontend

```bash
cd frontend
npm install
NEXT_PUBLIC_API_URL=http://localhost:8000 npm run dev
```

---

## A few routes

- `POST /api/upload` → upload a video
- `GET /api/jobs/{id}` → check status
- `GET /api/jobs/{id}/result` → get the splat link
- `GET /view/{id}` → full viewer
- `GET /embed/{id}` → iframe view

---

## Neural / vision bits

The rough flow is:

1. extract frames from the video
2. estimate camera motion / scene layout
3. train the 3D Gaussian Splat scene
4. export the final `.splat`

So it is mostly about AI vision, nural scene understanding, and 3D splats.

---

## GPU / server note

For the real reconstruction part, use:

- a local NVIDIA GPU machine
- or a remote GPU server

CPU-only will probably not be a fun time for the heavy part.