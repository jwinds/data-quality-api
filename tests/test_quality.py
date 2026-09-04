from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_quality_check_passes_for_valid_data():
    payload = {
        "records": [
            {
                "subject_id": "001",
                "status": "Alive",
            },
            {
                "subject_id": "002",
                "status": "Deceased",
            },
        ],
        "allowed_values_rules": [
            {
                "field": "status",
                "allowed_values": ["Alive", "Deceased"],
            }
        ],
    }

    response = client.post("/quality/check", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert data["record_count"] == 2
    assert all(result["passed"] for result in data["results"])


def test_quality_check_detects_duplicate_subject_id():
    payload = {
        "records": [
            {
                "subject_id": "001",
                "status": "Alive",
            },
            {
                "subject_id": "001",
                "status": "Deceased",
            },
        ],
        "allowed_values_rules": [
            {
                "field": "status",
                "allowed_values": ["Alive", "Deceased"],
            }
        ],
    }

    response = client.post("/quality/check", json=payload)

    assert response.status_code == 200

    results = response.json()["results"]

    duplicate_result = next(
        result
        for result in results
        if result["rule"] == "subject_id_unique"
    )

    assert duplicate_result["passed"] is False
    assert duplicate_result["failed_records"] == 1


def test_quality_check_detects_invalid_allowed_value():
    payload = {
        "records": [
            {
                "subject_id": "001",
                "status": "Unknown",
            }
        ],
        "allowed_values_rules": [
            {
                "field": "status",
                "allowed_values": ["Alive", "Deceased"],
            }
        ],
    }

    response = client.post("/quality/check", json=payload)

    assert response.status_code == 200

    results = response.json()["results"]

    status_result = next(
        result
        for result in results
        if result["rule"] == "status_allowed_values"
    )

    assert status_result["passed"] is False
    assert status_result["failed_records"] == 1

def test_quality_check_detects_null_subject_id():
    payload = {
        "records": [
            {
                "subject_id": None,
                "status": "Alive",
            }
        ],
        "allowed_values_rules": [
            {
                "field": "status",
                "allowed_values": ["Alive", "Deceased"],
            }
        ],
    }

    response = client.post("/quality/check", json=payload)

    assert response.status_code == 200

    results = response.json()["results"]

    null_result = next(
        result
        for result in results
        if result["rule"] == "subject_id_not_null"
    )

    assert null_result["passed"] is False
    assert null_result["failed_records"] == 1


def test_quality_check_rejects_malformed_request():
    payload = {
        "not_records": []
    }

    response = client.post("/quality/check", json=payload)

    assert response.status_code == 422