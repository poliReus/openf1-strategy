# LiveF1Strategy

**LiveF1Strategy** is a full-stack application to assist **race strategists** during live Formula 1 events.  
It ingests real-time telemetry (via [OpenF1](https://github.com/openf1)), computes and compares strategy options, and provides interactive dashboards to evaluate pit windows, tyre degradation, and SC/VSC responses.

---

## Features
- **Real-time ingestion** of OpenF1 telemetry (REST + WS/MQTT).
- **Strategy Engine** computing top-N race strategies with expected deltas and risks.
- **What-If Simulations** for pit-loss, tyre degradation, and safety-car scenarios.
- **Undercut/Overcut Analyzer** with probability estimates.
- **Interactive Dashboard** (React/Vite) with timelines, alerts, and tables.
- **Backtest Reports** for post-race analysis.
- **CI/CD ready** with Docker, Kubernetes, GitHub Actions.

---

## Tech Stack
- **Backend:** Python (FastAPI, Strawberry GraphQL), Kafka, Apache Arrow, Parquet, Postgres
- **Frontend:** React + Vite + Tailwind
- **ML:** TensorFlow (tyre degradation, pit-loss, probability models)
- **Infra:** Docker, K8s, Helm, GitHub Actions, Prometheus/Grafana

---

## Repository Structure
```
openf1-strategy/
├── ingest/          # OpenF1 clients (REST, WS, MQTT)
├── normalize/       # Arrow schemas & mappers
├── stream/          # Kafka producers/consumers
├── api/             # FastAPI + GraphQL
├── dashboard/       # React/Vite frontend
├── ml/              # ML models & notebooks
├── infra/           # Dockerfiles, Helm, K8s yamls
├── ops/             # Grafana, Prometheus, Kafka config
├── tests/           # Unit & integration tests
└── docs/            # System documentation
```

---

## Documentation
Full documentation: [docs/LiveF1Strategy_System_Documentation.md](docs/LiveF1Strategy_System_Documentation.md)

---

## Status
This project is under **active development**.  
First milestone: **ingestion pipeline prototype** with replayed race data.

---

## License
MIT
