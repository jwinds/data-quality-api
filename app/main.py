from fastapi import FastAPI

from app.models import QualityCheckRequest
from app.services import (
    check_null_subject_ids,
    check_duplicate_subject_ids,
    check_allowed_values,
)


app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.post("/quality/check")
def quality_check(request: QualityCheckRequest):
    results = [
        check_null_subject_ids(request.records),
        check_duplicate_subject_ids(request.records),
    ]

    for rule in request.allowed_values_rules:
        results.append(
            check_allowed_values(
                request.records,
                rule.field,
                rule.allowed_values,
            )
        )

    return {
        "record_count": len(request.records),
        "results": results,
    }