ACCEPTED_FIXES = [
    "for index in range(len(lines)):",
    "for index in range(0, len(lines)):",
    "for index in range( len(lines) ):",
    "for index in range(0,len(lines)):",
]

def grade_task2(action, target_line):
    if action.line_number != target_line:
        return 0.05, f"Fix must be applied to line {target_line}."
    
    if not action.fix_code:
        return 0.05, "Fix code is empty."
    
    normalized_fix = action.fix_code.strip()
    
    if any(normalized_fix.lower() == fix.lower().strip() for fix in ACCEPTED_FIXES):
         return 0.95, "Correct fix."
    
    # Check "valid python" but not in accepted fixes
    try:
        compile(normalized_fix, "<string>", "exec")
        return 0.3, "Syntactically valid Python, but not the correct fix."
    except SyntaxError:
        return 0.05, "Invalid Python syntax."


def grade(action_data: dict) -> float:
    """Wrapper for app.py to expose 'grade' with dict signature."""
    from server.models import Action
    action = Action(**action_data)
    # Task 2 targets: line 14
    score, _ = grade_task2(action, 14)
    return float(score)
