def check_null_subject_ids(records):
    null_count = sum(
        1 for record in records
        if record.get("subject_id") is None
    )

    return {
        "rule": "subject_id_not_null",
        "passed": null_count == 0,
        "failed_records": null_count,
    }

def check_duplicate_subject_ids(records):
    subject_ids = [
        record.get("subject_id")
        for record in records
        if record.get("subject_id") is not None
    ]

    duplicate_count = len(subject_ids) - len(set(subject_ids))

    return {
        "rule": "subject_id_unique",
        "passed": duplicate_count == 0,
        "failed_records": duplicate_count,
    }

def check_allowed_values(records, field, allowed_values):
    invalid_count = sum(
        1
        for record in records
        if record.get(field) not in allowed_values
    )

    return {
        "rule": f"{field}_allowed_values",
        "passed": invalid_count == 0,
        "failed_records": invalid_count,
    }