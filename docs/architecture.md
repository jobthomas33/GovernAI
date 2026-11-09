# Architecture

## Current request flow

```mermaid
flowchart LR
    Client[HTTP client] --> API[FastAPI /api/v1]
    API --> Services[Governance services]
    Services --> ORM[SQLAlchemy models]
    ORM --> DB[(SQLite local / PostgreSQL Docker)]
    Services --> Audit[Audit events]
    Audit --> DB
    Migrations[Alembic] --> DB
```

Routers validate requests and shape responses. Services implement business rules and write domain changes and their audit events in one transaction. Alembic manages durable schema upgrades; metadata creation at app startup keeps a fresh local SQLite run convenient.

## Roadmap

```mermaid
flowchart LR
    MVP[GovernAI v0.1 API] --> Auth[Authentication and roles]
    Auth --> UI[Governance web interface]
    UI --> Integrations[Data and model platform integrations]
    Integrations --> Deployment[Cloud deployment and operations]
```
