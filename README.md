# GovernAI

GovernAI is a small AI governance registry API. It gives teams one place to register AI systems, record structured risk assessments, track governance work, and keep an audit trail of important changes.

## v0.1 features

- Create, list, update, and delete AI systems.
- Record and update risk assessments with deterministic risk scoring.
- Track checklist items and completion dates.
- Automatically create audit events for system, assessment, and checklist changes.
- Summarize risk counts, checklist completion, and recent audit activity.
- Run locally on SQLite or use PostgreSQL with Docker Compose.

There is no frontend, authentication, chatbot, data-platform integration, or cloud deployment in this MVP.

## Tech stack

Python 3.11+, FastAPI, Pydantic, SQLAlchemy 2, Alembic, SQLite/PostgreSQL, pytest.

## Run locally

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
uvicorn app.main:app --reload
```

The default database is `./governai.db`. A fresh local database is initialized when the application starts. For schema upgrades on an existing database, run:

```powershell
alembic upgrade head
```

Open <http://127.0.0.1:8000/docs> for interactive API documentation. The health endpoint is <http://127.0.0.1:8000/health>.

## Docker with PostgreSQL

```powershell
docker compose up --build
```

Compose starts PostgreSQL and the API. The app runs Alembic migrations before starting Uvicorn. The development database credentials are declared in `docker-compose.yml`; change them before using this setup beyond local development.

## Tests

```powershell
python -m pip install -e ".[dev]"
pytest
pytest --cov=app --cov-report=term-missing
```

Tests use an isolated in-memory SQLite database.

## Risk scoring

Each assessment receives points for governance risk factors:

| Factor | Points |
| --- | ---: |
| Personal data is used | 20 |
| Automated decision making is used | 25 |
| Customers are impacted | 20 |
| Human oversight is absent | 20 |
| Transparency is unavailable | 15 |
| Monitoring is disabled | 15 |

Scores map to `LOW` (0–29), `MEDIUM` (30–59), and `HIGH` (60+). The maximum is 115. Risk levels on the dashboard use each system's most recently created assessment; systems without an assessment are not included in risk-level counts.

## API example

```powershell
$system = Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/api/v1/systems `
  -ContentType 'application/json' -Body '{"name":"Claims Triage","owner":"A. Owner","department":"Claims","business_purpose":"Prioritize incoming claims"}'

Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/v1/systems/$($system.id)/assessments" `
  -ContentType 'application/json' -Body '{"personal_data_usage":true,"automated_decision_making":true,"customer_impact":false,"human_oversight":true,"transparency_available":true,"monitoring_enabled":true}'
```

Full endpoint list and schemas are in [docs/api.md](docs/api.md). See [docs/architecture.md](docs/architecture.md) and [docs/data-model.md](docs/data-model.md) for design details.

## Roadmap

1. Authentication, authorization, and role-based access.
2. Web dashboard and richer assessment workflows.
3. Integrations with model inventories, data catalogs, and monitoring tools.
4. Production deployment, observability, and operational hardening.
