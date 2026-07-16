# FinSight — Multi-Agent Financial Anomaly Detection & Commentary

A multi-agent pipeline that detects anomalies in financial time-series data,
explains the drivers behind them, and generates executive commentary — built
with **LangGraph**, **scikit-learn**, and the **Gemini API**, served via **Flask**.

## Why this exists

Three specialist agents collaborate in a LangGraph state machine:

```
  [Anomaly Agent]  →  [Driver Agent]  →  [Commentary Agent]
   scikit-learn        variance /          Gemini API
   IsolationForest     line-item           executive
   + robust z-score    attribution         narrative
```

The ML/stats agents compute trustworthy numbers; the LLM agent only *narrates*
those numbers (it never invents figures). That separation keeps the output
auditable — a deliberate design choice for a finance context.

## Architecture

| File | Role |
|---|---|
| `agents/anomaly.py` | IsolationForest + robust z-score detector (predictive ML) |
| `agents/drivers.py` | Deterministic variance/driver decomposition per anomaly |
| `agents/commentary.py` | LLM commentary (Gemini), with templated fallback if no API key |
| `graph.py` | LangGraph orchestration: typed shared state + explicit hand-offs |
| `data_utils.py` | CSV loader + synthetic finance data generator |
| `app.py` | Flask API + minimal demo UI |

## Run locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-...     # optional; omit to use the templated fallback
python app.py
# open http://localhost:5000
```

Leave the file input empty to run on built-in synthetic finance data, or upload
a tidy CSV with columns: `period, category, value`.

## API

```bash
# synthetic run
curl -X POST http://localhost:5000/analyze

# your own data
curl -X POST -F "file=@your_data.csv" http://localhost:5000/analyze
```

Returns JSON: `detection` (raw ML output), `findings` (with drivers), and
`commentary` (LLM narrative).

## Deploy to Render

1. Push this folder to a GitHub repo.
2. In Render: **New → Web Service → connect the repo**. Render reads
   `render.yaml` automatically (or set Build `pip install -r requirements.txt`,
   Start `gunicorn app:app --bind 0.0.0.0:$PORT --timeout 120`).
3. Add a secret env var **`ANTHROPIC_API_KEY`** in the dashboard.
4. Deploy → you get a live URL. Put that URL on your resume/GitHub.

Health check endpoint: `GET /health`.

## Note on the synthetic data

The generator sums categories to a small net total, so period-over-period %
changes on the *net* series can look extreme (small denominator). This is a
demo-data artifact. For cleaner headline numbers, point the anomaly detector at
a single series (e.g. Revenue) instead of the net total — one-line change in
`app.py`/`graph.py` where `long_df` is built.

## Resume bullet

> **FinSight – Multi-Agent Financial Anomaly & Commentary System** — Built a
> multi-agent pipeline (**LangGraph**) where specialized agents perform
> ML-based anomaly detection (**scikit-learn** IsolationForest), variance/driver
> analysis, and **LLM-generated executive commentary** (Gemini API) on financial
> time-series data; deployed as a live **Flask** service on Render.
