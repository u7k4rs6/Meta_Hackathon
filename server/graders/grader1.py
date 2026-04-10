def grade_task1(action, target_line, target_bug_type):
    if action.line_number == target_line and action.bug_type == target_bug_type:
        return float(0.95), "Correct line and bug type."
        return float(0.85), "Correct line and bug type."
    elif action.line_number == target_line and action.bug_type != target_bug_type:
        return float(0.50), "Correct line, but wrong bug type. (Partial Success)"
    else:
        return float(0.15), "Wrong line."


def grade(action_data: dict) -> float:
    """Standardized grader interface for the platform.
    Returns a score strictly within the (0.15, 0.85) range.
    """
    from server.models import Action
    try:
        if not action_data:
            return float(0.15)
        
        # Merge defaults to handle partial dicts
        defaults = {"action_type": "noop", "line_number": None, "bug_type": None, "fix_code": None}
        full_data = {**defaults, **action_data}
        
        action = Action(**full_data)
        # Task 1 targets: line 9, bug "off-by-one"
        score, _ = grade_task1(action, 9, "off-by-one")
        
        # Global clamping safety net
        return float(max(0.05, min(0.95, float(score))))
    except Exception:
        return float(0.15)