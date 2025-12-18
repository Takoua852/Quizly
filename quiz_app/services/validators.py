def is_valid_quiz_payload(data) -> bool:
    """
    Validate the structure and content of generated quiz data.

    Validation rules:
    - Data must be a list of exactly 10 items
    - Each item must be a dictionary
    - Each question must contain exactly 4 unique options
    - The correct answer must match one of the options

    Args:
        data (list): Parsed JSON data returned by the LLM.

    Returns:
        bool: True if the quiz data is valid, otherwise False.
    """
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
