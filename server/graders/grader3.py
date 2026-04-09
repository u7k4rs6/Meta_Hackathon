"""Grader for task3_hard – multi-bug identification in auth service."""

# The primary bug (based on task description) is the 'wrong-operator' logic:
# expires_in: -1 instead of 3600.
# The secondary bug is the 'null-deref' (KeyError) in the dictionary access.

BUG_LINE = 13
PRIMARY_BUG_TYPE = "wrong-operator"
SECONDARY_BUG_TYPES = ["null-deref", "missing-return"]

# Accepted fixes for the primary bug (line 13)
ACCEPTED_FIXES = [
    'return {"token": token, "expires_in": 3600}',
    'return {"token":token,"expires_in":3600}',
    "return {'token': token, 'expires_in': 3600}",
]


def grade_task3(action):
    """Grade a task-3 action.
    Returns (score, feedback) where score is strictly in (0, 1).
    """
    # --- click_line path (identify the bug) ---
    if action.action_type == "click_line":
        if action.line_number is None or action.bug_type is None:
            return 0.1, "Incomplete click_line action."

        line_ok = action.line_number == BUG_LINE
        type_ok = action.bug_type == PRIMARY_BUG_TYPE
        type_partial = action.bug_type in SECONDARY_BUG_TYPES
        
        # Also reward identifying the other bug (line 8)
        is_other_bug = (action.line_number == 8 and action.bug_type == "null-deref")

        if line_ok and type_ok:
            return 0.95, "Correct – identified the wrong-operator bug."
        elif is_other_bug:
            return 0.8, "Correct – identified the key-access bug (secondary bug)."
        elif line_ok and type_partial:
            return 0.7, "Correct line, related bug type but not the primary one."
        elif line_ok:
            return 0.6, "Correct line, but wrong bug type. (Partial Success)"
        elif type_ok:
            return 0.6, "Right bug type, but wrong line. (Partial Success)"
        else:
            return 0.1, "Wrong line and wrong bug type."

    # --- submit_fix path ---
    if action.action_type == "submit_fix":
        if action.line_number is None or not action.fix_code:
            return 0.1, "Incomplete submit_fix action."

        if action.line_number != BUG_LINE:
            # If they fix the other bug (line 8)
            if action.line_number == 8 and "password_hash" in action.fix_code:
                return 0.8, "Correctly fixed the secondary key-access bug."
            return 0.2, f"Target line {action.line_number} is not the primary bug."

        normalized = action.fix_code.strip()
        if any(normalized.lower() == fix.lower() for fix in ACCEPTED_FIXES):
            return 0.95, "Correct fix applied."

        # Syntactically valid but not the ideal fix
        try:
            compile(normalized, "<string>", "exec")
            return 0.6, "Syntactically valid Python, but not the expected fix. (Partial Success)"
        except SyntaxError:
            return 0.1, "Invalid Python syntax."

    # noop or unknown
    return 0.1, "No meaningful action taken."


def grade(action_data: dict) -> float:
    """Standardized grader interface for the platform.
    Returns a score strictly within the (0.01, 0.99) range.
    """
    from server.models import Action
    try:
        action = Action(**action_data)
        score, _ = grade_task3(action)
        # Global clamping safety net
        return max(0.01, min(0.99, float(score)))
    except Exception:
        return 0.1

