def evaluate_status(result, expected_status):
    return result.get("status") == expected_status


def evaluate_source(result, expected_source_contains):
    if not expected_source_contains:
        return True

    sources = result.get("sources", [])
    return any(expected_source_contains in src for src in sources)