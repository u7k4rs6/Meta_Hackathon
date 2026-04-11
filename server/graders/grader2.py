def _clamp(score: float) -> float:
    """Clamp score to be strictly within (0, 1). Never returns 0.0 or 1.0."""
    return float(max(0.01, min(0.99, float(score))))


ACCEPTED_FIXES = [
    "for index in range(len(lines)):",
    "for index in range(0, len(lines)):",
    "for index in range( len(lines) ):",
    "for index in range(0,len(lines)):",
]


def grade_task2(action, target_line):
    if action.line_number != target_line:
        return 0.2, f"Fix must be applied to line {target_line}."

    if not action.fix_code:
        return 0.2, "Fix code is empty."

    normalized_fix = action.fix_code.strip()

    if any(normalized_fix.lower() == fix.lower().strip() for fix in ACCEPTED_FIXES):
        return 0.75, "Correct fix."

    # Check "valid python" but not in accepted fixes
    try:
        compile(normalized_fix, "<string>", "exec")
        return 0.5, "Syntactically valid Python, but not the correct fix. (Partial Success)"
    except SyntaxError:
        return 0.2, "Invalid Python syntax."


def grade(action_data: dict) -> float:
    """Standardized grader interface for the platform.
    Returns a score strictly within (0, 1) — never 0.0 or 1.0.
    """
    from server.models import Action
    try:
        if not action_data:
            return _clamp(0.2)

        # Merge defaults to handle partial dicts
        defaults = {"action_type": "noop", "line_number": None, "bug_type": None, "fix_code": None}
        full_data = {**defaults, **action_data}

        action = Action(**full_data)
        # Task 2 targets: line 14
        score, _ = grade_task2(action, 14)
        return _clamp(score)
    except Exception:
        return _clamp(0.2)
