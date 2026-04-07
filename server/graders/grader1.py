def grade_task1(action, target_line, target_bug_type):
    if action.line_number == target_line and action.bug_type == target_bug_type:
        return 0.99, "Correct line and bug type."
    elif action.line_number == target_line and action.bug_type != target_bug_type:
        return 0.5, "Correct line, but wrong bug type."
    else:
        return 0.01, "Wrong line."


def grade(action_data: dict) -> float:
    """Standardized grader entry point for task1_easy.

    Evaluates whether the agent correctly identified the off-by-one bug.
    Returns a score strictly between 0 and 1 (exclusive).
    """
    TARGET_LINE = 9
    TARGET_BUG_TYPE = "off-by-one"

    line_number = action_data.get("line_number")
    bug_type = action_data.get("bug_type", "")

    if line_number == TARGET_LINE and bug_type == TARGET_BUG_TYPE:
        return 0.99
    elif line_number == TARGET_LINE and bug_type != TARGET_BUG_TYPE:
        return 0.5
    else:
        return 0.01
