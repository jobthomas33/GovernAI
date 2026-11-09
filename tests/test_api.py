from tests.conftest import assessment_payload, system_payload


def test_create_update_delete_system_and_audit(client):
    created = client.post("/api/v1/systems", json=system_payload())
    assert created.status_code == 201
    system_id = created.json()["id"]
    updated = client.put(f"/api/v1/systems/{system_id}", json={"department": "Risk"})
    assert updated.status_code == 200
    assert updated.json()["department"] == "Risk"
    assert client.get(f"/api/v1/systems/{system_id}/audit-events").json()[1]["action"] == "UPDATE"
    assert client.delete(f"/api/v1/systems/{system_id}").status_code == 204


def test_assessment_score_is_calculated_and_updates(client):
    system_id = client.post("/api/v1/systems", json=system_payload()).json()["id"]
    response = client.post(f"/api/v1/systems/{system_id}/assessments", json=assessment_payload())
    assert response.status_code == 201
    assert (response.json()["risk_score"], response.json()["risk_level"]) == (115, "HIGH")
    assessment_id = response.json()["id"]
    changed = client.put(f"/api/v1/assessments/{assessment_id}", json=assessment_payload(
        automated_decision_making=False, customer_impact=False, human_oversight=True,
        transparency_available=True, monitoring_enabled=True))
    assert (changed.json()["risk_score"], changed.json()["risk_level"]) == (20, "LOW")


def test_checklist_completion_and_dashboard(client):
    system_id = client.post("/api/v1/systems", json=system_payload()).json()["id"]
    client.post(f"/api/v1/systems/{system_id}/checklist-items", json={"item_name": "Impact review", "is_completed": True})
    client.post(f"/api/v1/systems/{system_id}/checklist-items", json={"item_name": "Monitoring plan"})
    summary = client.get("/api/v1/dashboard/summary").json()
    assert summary["total_systems"] == 1
    assert summary["checklist_completion_percent"] == 50
    assert len(summary["recent_audit_events"]) == 3


def test_empty_name_is_rejected(client):
    assert client.post("/api/v1/systems", json=system_payload() | {"name": "  "}).status_code == 422


def test_empty_system_list_and_audit_endpoint(client):
    assert client.get("/api/v1/systems").json() == []
    assert client.get("/api/v1/audit-events").json() == []
