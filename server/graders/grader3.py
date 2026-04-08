"""Grader for task3_hard – multi-bug identification in auth service."""

# The primary bug is accessing user_db[username]["password"] instead of
# user_db[username]["password_hash"], which causes a KeyError (null-deref class).
# Target line in the diff is line 11 (the changed key access line).

BUG_LINE = 11
PRIMARY_BUG_TYPE = "null-deref"
SECONDARY_BUG_TYPES = ["wrong-operator", "missing-return"]

# Accepted fixes: restore the correct dict key
ACCEPTED_FIXES = [
    'stored_hash = user_db[username]["password_hash"]',
    "stored_hash = user_db[username]['password_hash']",
    'stored_hash = user_db[username].get("password_hash")',
    "stored_hash = user_db[username].get('password_hash')",
]


def grade_task3(action):
    """Grade a task-3 action.

    Returns (score, feedback) where score is strictly in (0, 1).
    """
    # --- click_line path (identify the bug) ---
    if action.action_type == "click_line":
        if action.line_number is None or action.bug_type is None:
            return 0.05, "Incomplete click_line action."

        line_ok = action.line_number == BUG_LINE
        type_ok = action.bug_type == PRIMARY_BUG_TYPE
        type_partial = action.bug_type in SECONDARY_BUG_TYPES

        if line_ok and type_ok:
            return 0.95, "Correct – identified the key-access bug."
        elif line_ok and type_partial:
            return 0.6, "Correct line, related bug type but not the primary one."
        elif line_ok:
            return 0.4, "Correct line, but wrong bug type."
        elif type_ok:
            return 0.3, "Right bug type, but wrong line."
        else:
            return 0.1, "Wrong line and wrong bug type."

    # --- submit_fix path ---
    if action.action_type == "submit_fix":
        if action.line_number is None or not action.fix_code:
            return 0.05, "Incomplete submit_fix action."

        if action.line_number != BUG_LINE:
            return 0.1, f"Fix must target line {BUG_LINE}."

        normalized = action.fix_code.strip()
        if any(normalized.lower() == fix.lower() for fix in ACCEPTED_FIXES):
            return 0.95, "Correct fix applied."

        # Syntactically valid but not the ideal fix
        try:
            compile(normalized, "<string>", "exec")
            return 0.4, "Syntactically valid Python, but not the expected fix."
        except SyntaxError:
            return 0.1, "Invalid Python syntax."

    # noop or unknown
    return 0.05, "No meaningful action taken."


def grade(action_data: dict) -> float:
    """Wrapper for app.py to expose 'grade' with dict signature."""
    from server.models import Action
    action = Action(**action_data)
    score, _ = grade_task3(action)
    return float(score)
