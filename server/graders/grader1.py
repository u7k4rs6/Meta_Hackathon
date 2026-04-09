def grade_task1(action, target_line, target_bug_type):
    if action.line_number == target_line and action.bug_type == target_bug_type:
        return 0.95, "Correct line and bug type."
    elif action.line_number == target_line and action.bug_type != target_bug_type:
        return 0.65, "Correct line, but wrong bug type. (Partial Success)"
    else:
        return 0.1, "Wrong line."


def grade(action_data: dict) -> float:
    """Standardized grader interface for the platform.
    Returns a score strictly within the (0.01, 0.99) range.
    """
    from server.models import Action
    try:
        action = Action(**action_data)
        # Task 1 targets: line 9, bug "off-by-one"
        score, _ = grade_task1(action, 9, "off-by-one")
        # Global clamping safety net
        return max(0.01, min(0.99, float(score)))
    except Exception:
        return 0.1