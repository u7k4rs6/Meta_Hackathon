from server.models import Action

def grade_task3(action: Action):
    # Targets based on task3_hard.diff
    primary_bug_line = 36
    primary_bug_type = "dictionary-key-error"
    
    # Check for correct click action
    if action.action_type == "click_line":
        if action.line_number == primary_bug_line:
            if action.bug_type == primary_bug_type:
                return float(0.7), "Correct – Identified the wrong dictionary key bug."
            else:
                return float(0.5), f"Correct line ({primary_bug_line}), but '{action.bug_type}' is wrong."
        return float(0.3), f"Line {action.line_number} is not the primary bug."
    
    # Check for correct fix
    elif action.action_type == "submit_fix":
        if action.line_number != primary_bug_line:
            return float(0.3), f"Fix must be applied to line {primary_bug_line}."
        
        if not action.fix_code:
             return float(0.3), "Fix code is empty."
        
        normalized_fix = action.fix_code.strip()
        # Correct fix: user_id = payload.get("sub") or user_id = payload["sub"]
        if 'payload.get("sub")' in normalized_fix or 'payload["sub"]' in normalized_fix:
            return float(0.7), "Correct fix - using 'sub' instead of 'user_id' in JWT payload."
        return float(0.5), "Syntactically correct fix, but doesn't solve the payload key issue."

    return float(0.3), "No meaningful action taken."

def grade(action_data: dict) -> float:
    """Standardized grader interface for the platform.
    Returns a score strictly within the (0.1, 0.9) range.
    """
    from server.models import Action
    try:
        if not action_data:
            return float(0.3)
            
        # Merge defaults to handle partial dicts
        defaults = {"action_type": "noop", "line_number": None, "bug_type": None, "fix_code": None}
        full_data = {**defaults, **action_data}
        
        action = Action(**full_data)
        score, _ = grade_task3(action)
        
        # Safe padding within the (0.1, 0.9) range
        return float(max(0.1, min(0.9, float(score))))
    except Exception:
        return float(0.3)
