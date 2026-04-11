def _clamp(score: float) -> float:
    """Clamp score to be strictly within (0, 1). Never returns 0.0 or 1.0."""
    return float(max(0.01, min(0.99, float(score))))


def grade_task1(action, target_line, target_bug_type):
    if action.line_number == target_line and action.bug_type == target_bug_type:
        return 0.75, "Correct line and bug type."
    elif action.line_number == target_line and action.bug_type != target_bug_type:
        return 0.5, "Correct line, but wrong bug type. (Partial Success)"
    else:
        return 0.2, "Wrong line."


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
        # Task 1 targets: line 9, bug "off-by-one"
        score, _ = grade_task1(action, 9, "off-by-one")
        return _clamp(score)
    except Exception:
        return _clamp(0.2)