# API reference

Interactive OpenAPI documentation is available at `/docs` while the server is running.

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET, POST | `/api/v1/systems` | List and register systems |
| GET, PUT, DELETE | `/api/v1/systems/{id}` | Read, update, and delete a system |
| POST, GET | `/api/v1/systems/{id}/assessments` | Create and list assessments |
| GET, PUT | `/api/v1/assessments/{assessment_id}` | Read and recalculate an assessment |
| POST, GET | `/api/v1/systems/{id}/checklist-items` | Create and list checklist items |
| PUT, DELETE | `/api/v1/checklist-items/{item_id}` | Update and delete checklist items |
| GET | `/api/v1/audit-events` | List recent audit events (`limit` 1–200) |
| GET | `/api/v1/systems/{id}/audit-events` | List events belonging to a system |
| GET | `/api/v1/dashboard/summary` | Dashboard counts and recent events |
| GET | `/health` | Liveness check |

Example system:

```json
{
  "name": "Claims Triage",
  "owner": "A. Owner",
  "department": "Claims",
  "business_purpose": "Prioritize incoming claims",
  "technology_stack": "Python, scikit-learn",
  "deployment_status": "pilot"
}
```

Risk assessments require the six boolean factors described in the README. The API calculates `risk_score` and `risk_level`; clients cannot submit their own values.
