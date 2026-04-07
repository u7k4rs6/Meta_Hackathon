def grade_task3(action, target_line, target_bug_type):
    if action.line_number == target_line and action.bug_type == target_bug_type:
        return 1.0, "Correct line and bug type identified."
    elif action.line_number == target_line:
        return 0.5, "Correct line, wrong bug type."
    else:
        return 0.0, "Wrong line flagged."
