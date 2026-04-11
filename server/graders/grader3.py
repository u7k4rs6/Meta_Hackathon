def _clamp(score: float) -> float:
    """Clamp score to be strictly within (0, 1). Never returns 0.0 or 1.0."""
    return float(max(0.01, min(0.99, float(score))))


def grade_task3(action):
    primary_bug_line = 36
    primary_bug_type = "dictionary-key-error"

    if action.action_type == "click_line":
        if action.line_number == primary_bug_line:
            if action.bug_type == primary_bug_type:
                return 0.75, "Correct – Identified the wrong dictionary key bug."
            return 0.5, f"Correct line ({primary_bug_line}), but '{action.bug_type}' is wrong."
        return 0.2, f"Line {action.line_number} is not the primary bug."

    elif action.action_type == "submit_fix":
        if action.line_number != primary_bug_line:
            return 0.2, f"Fix must be applied to line {primary_bug_line}."
        if not action.fix_code:
            return 0.2, "Fix code is empty."
        normalized_fix = action.fix_code.strip()
        if 'payload.get("sub")' in normalized_fix or 'payload["sub"]' in normalized_fix:
            return 0.75, "Correct fix - using 'sub' instead of 'user_id' in JWT payload."
        return 0.5, "Syntactically correct fix, but doesn't solve the payload key issue."

    # Explicit fallthrough for noop and any unknown action_type
    return 0.2, "No meaningful action taken."


def grade(action_data: dict) -> float:
    """Standardized grader interface for the platform.
    Returns a score strictly within (0, 1) — never 0.0 or 1.0.
    """
    from server.models import Action
    try:
        if not action_data:
            return _clamp(0.2)

        # Merge defaults to handle partial dicts
        defaults = {"action_type": "noop", "line_number": None, "bug_type": None, "fix_code": None}
        full_data = {**defaults, **action_data}

        action = Action(**full_data)
        score, _ = grade_task3(action)
        return _clamp(score)
    except Exception:
        return _clamp(0.2)
