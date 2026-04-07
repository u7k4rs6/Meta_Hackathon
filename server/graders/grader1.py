def grade_task1(action, target_line, target_bug_type):
    if action.line_number == target_line and action.bug_type == target_bug_type:
        return 0.99, "Correct line and bug type."
    elif action.line_number == target_line and action.bug_type != target_bug_type:
        return 0.5, "Correct line, but wrong bug type."
    else:
        return 0.01, "Wrong line."
