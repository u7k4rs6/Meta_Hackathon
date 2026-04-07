ACCEPTED_FIXES = [
    "for index in range(len(lines)):",
    "for index in range(0, len(lines)):",
    "for index in range( len(lines) ):",
    "for index in range(0,len(lines)):",
]

def grade_task2(action, target_line):
    if action.line_number != target_line:
        return 0.01, f"Fix must be applied to line {target_line}."
    
    if not action.fix_code:
        return 0.01, "Fix code is empty."
    
    normalized_fix = action.fix_code.strip()
    
    if any(normalized_fix.lower() == fix.lower().strip() for fix in ACCEPTED_FIXES):
         return 0.99, "Correct fix."
    
    # Check "valid python" but not in accepted fixes
    try:
        compile(normalized_fix, "<string>", "exec")
        return 0.3, "Syntactically valid Python, but not the correct fix."
    except SyntaxError:
        return 0.01, "Invalid Python syntax."
