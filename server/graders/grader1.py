def grade_task1(action, target_line, target_bug_type):
    if action.line_number == target_line and action.bug_type == target_bug_type:
        return 0.95, "Correct line and bug type."
    elif action.line_number == target_line and action.bug_type != target_bug_type:
        return 0.5, "Correct line, but wrong bug type."
    else:
        return 0.05, "Wrong line."


def grade(action_data: dict) -> float:
    """Wrapper for app.py to expose 'grade' with dict signature."""
    from server.models import Action
    action = Action(**action_data)
    # Task 1 targets: line 9, bug "off-by-one"
    score, _ = grade_task1(action, 9, "off-by-one")
    return float(score)
