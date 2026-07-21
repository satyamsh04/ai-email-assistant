# System Architecture

The project has two local runtime paths:

```text
Outlook add-in (https://localhost:3000)
  ├─ chat and draft reply
  │    └─ OpenClaw gateway (:18789) ── Ollama
  └─ Auto Label
       └─ Webpack /ml-api proxy ── FastAPI (:8000) ── priority ranker
                                     └─ feedback_log.csv
```

## Outlook add-in

`addin/` contains the Office.js task pane, Outlook manifest, Webpack
configuration, and Jest tests. Moving the files does not change manifest
resource URLs because Webpack still serves `taskpane.html` and `commands.html`
from `https://localhost:3000`.

## Recommendation service

`ml/src/inference.py` exposes the prediction and feedback API. A trained model
combines local TF-IDF text vectors with deterministic metadata features and a
multiclass logistic-regression classifier. No external embedding API is used.

If `ml/models/priority_ranker.joblib` is absent, inference uses transparent
rules so the endpoint remains usable before the first training run. Training
combines `seed_emails.json` with valid corrections from `feedback_log.csv`.

## Failure handling

If the Python service is unavailable, Auto Label falls back to the existing
OpenClaw/Ollama prompt. Chat and draft-reply behavior do not depend on the ML
service. The optional `gateway/` bridge provides a standalone Node endpoint for
clients that should not connect to FastAPI directly.
