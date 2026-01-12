def is_valid_quiz_payload(data) -> bool:
    """Check if quiz data is valid: list of 10 dicts with 4 unique options and a correct answer."""

    if not isinstance(data, list) or len(data) != 10:
        return False

    for q in data:
        if not isinstance(q, dict):
            return False

        options = q.get("question_options", [])
        answer = q.get("answer")

        if (
            not isinstance(options, list)
            or len(options) != 4
            or len(set(options)) != 4
            or answer not in options
        ):
            return False

    return True
