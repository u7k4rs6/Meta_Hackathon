ACCEPTED_FIXES = [
    "for index in range(len(lines)):",
    "for index in range(0, len(lines)):",
    "for index in range( len(lines) ):",
    "for index in range(0,len(lines)):",
]

def grade_task2(action, target_line):
    if action.line_number != target_line:
        return float(0.15), f"Fix must be applied to line {target_line}."
    
    if not action.fix_code:
        return float(0.15), "Fix code is empty."
    
    normalized_fix = action.fix_code.strip()
    
    if any(normalized_fix.lower() == fix.lower().strip() for fix in ACCEPTED_FIXES):
         return float(0.95), "Correct fix."
    
    # Check "valid python" but not in accepted fixes
    try:
        compile(normalized_fix, "<string>", "exec")
        return float(0.65), "Syntactically valid Python, but not the correct fix. (Partial Success)"
    except SyntaxError:
        return float(0.15), "Invalid Python syntax."


def grade(action_data: dict) -> float:
    """Standardized grader interface for the platform.
    Returns- [x] Harden `grader1.py`: strict float enforcement and robust `grade` function
- [x] Harden `grader2.py`: strict float enforcement and robust `grade` function
    """
    from server.models import Action
    try:
        if not action_data:
            return float(0.15)
            
        # Merge defaults to handle partial dicts
        defaults = {"action_type": "noop", "line_number": None, "bug_type": None, "fix_code": None}
        full_data = {**defaults, **action_data}
        
        action = Action(**full_data)
        # Task 2 targets: line 14
        score, _ = grade_task2(action, 14)
        
        # Global clamping safety net
        return float(max(0.05, min(0.95, float(score))))
    except Exception:
        return float(0.15)

