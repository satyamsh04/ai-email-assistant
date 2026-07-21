# AI Email Assistant

A local-first Outlook add-in with an optional machine-learning service for
email-priority recommendations. The add-in uses Office.js and OpenClaw/Ollama;
the Python service learns from labelled email examples and user feedback.

## Repository layout

```text
addin/    Outlook add-in, tests, manifest, and Webpack dev server
ml/       FastAPI recommendation service, training code, data, and models
gateway/  Optional Node.js API bridge
docs/     Architecture and project documentation
```

## Prerequisites

- Node.js 18+
- Python 3.10+
- Outlook Desktop with Microsoft 365
- Ollama with the `qwen2.5:3b` model

## Outlook add-in

```powershell
cd addin
npm install
npm run setup
npm start
```

In another terminal, run `npm run gateway` from `addin`. Sideload
`addin/manifest.xml` in Outlook. Runtime URLs remain under
`https://localhost:3000`, so moving the manifest does not change them.

## ML recommendation service

```powershell
cd ml
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m src.train_ranker
uvicorn src.inference:app --reload --port 8000
```

The service exposes:

- `GET /health` for readiness
- `POST /recommend` for Urgent/Medium/Minor predictions
- `POST /feedback` to append corrected labels to `ml/data/feedback_log.csv`

When the service is available, the add-in's `/ml-api` Webpack proxy uses it for
Auto Label. If it is unavailable, the add-in falls back to OpenClaw/Ollama.

## Optional Node bridge

```powershell
cd gateway
npm install
npm start
```

The bridge listens on port 3001 and forwards `/api/ml/*` to the Python service.

## Tests

```powershell
cd addin
npm test -- --runInBand
npm run build

cd ..\ml
python -m unittest discover -s tests
```

## Privacy

Email data stays on the local machine unless you deliberately configure an
external model or deploy these services remotely. Feedback logs can contain
email metadata and should not be committed with real user content.
