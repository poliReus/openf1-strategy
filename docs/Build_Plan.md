# LiveF1Strategy — Step-by-Step Build Plan

## Phase 0 — Setup
- [ ] Create mono-repo `openf1-strategy/`
- [ ] Initialize GitHub repo + PR template, pre-commit hooks (Black, Ruff, Mypy).
- [ ] Add CI skeleton (GitHub Actions: lint + test).

## Phase 1 — Ingestion
- [ ] Implement Python service `ingest/`:
  - REST pull of historical race.
  - WS/MQTT subscription for live data.
- [ ] Normalize to **Arrow** schema (`telemetry.raw`).
- [ ] Produce to Kafka topic `telemetry.raw`.
- [ ] Unit test: schema compliance.

## Phase 2 — Normalization & Storage
- [ ] Build `normalize/` lib:
  - Map raw to enriched schema (`telemetry.normalized`).
  - Add stint, compound, gaps.
- [ ] Store to Parquet (partitioned).
- [ ] Integration test: replay 1 full race.

## Phase 3 — Strategy Engine MVP
- [ ] Create `stream/` consumer:
  - Subscribe `telemetry.normalized`.
  - Compute deterministic strategies (heuristics).
- [ ] Publish to Kafka topic `strategy.options`.
- [ ] Add tests: recompute after every new lap.

## Phase 4 — API Layer
- [ ] Setup `api/` with FastAPI.
- [ ] Expose GraphQL with Strawberry:
  - `liveOptions`, `whatIf`, `undercutChance`.
- [ ] Secure with JWT.
- [ ] Test resolvers with mocked Kafka.

## Phase 5 — Frontend
- [ ] Scaffold `dashboard/` with React + Vite.
- [ ] Implement **Driver Detail** view:
  - Option table, stint timeline.
- [ ] Add GraphQL client.
- [ ] Live refresh on subscription.

## Phase 6 — Advanced Services
- [ ] Add **What-If** microservice.
- [ ] Add **Undercut/Overcut** service.
- [ ] Add SC/VSC handler.
- [ ] Extend GraphQL.

## Phase 7 — ML Models
- [ ] Implement tyre degradation predictor (TensorFlow).
- [ ] Pit-loss model with SC modifiers.
- [ ] Logistic undercut success model.
- [ ] Integrate with engine outputs.

## Phase 8 — Backtesting
- [ ] Build batch jobs over Parquet.
- [ ] Generate HTML/PDF post-race reports.
- [ ] Compare chosen vs model-optimal strategies.

## Phase 9 — Ops & Deployment
- [ ] Add Dockerfiles per service.
- [ ] Helm chart for K8s deployment.
- [ ] Observability: Prometheus metrics, Grafana dashboards.
- [ ] Kafka monitoring: lag alerts.

## Phase 10 — Polish
- [ ] Role-based access (strategist, engineer, analyst).
- [ ] Locking & commenting on strategy options.
- [ ] Polish UI with alerts & what-if sliders.
- [ ] Finalize documentation.
