import sys
import os

# Add the current directory to sys.path so we can import 'server'
sys.path.append(os.getcwd())

try:
    from server.graders.grader1 import grade as grade1
    from server.graders.grader2 import grade as grade2
    from server.graders.grader3 import grade as grade3
    
    print("Grader 1 import: SUCCESS")
    print("Grader 2 import: SUCCESS")
    print("Grader 3 import: SUCCESS")
    
    # Test with dummy data
    dummy_action = {
        "action_type": "noop",
        "line_number": None,
        "bug_type": None,
        "fix_code": None
    }
    
    s1 = grade1(dummy_action)
    s2 = grade2(dummy_action)
    s3 = grade3(dummy_action)
    
    print(f"Grader 1 score: {s1}")
    print(f"Grader 2 score: {s2}")
    print(f"Grader 3 score: {s3}")
    
    if all(0 < s < 1 for s in [s1, s2, s3]):
        print("All scores are strictly between 0 and 1.")
    else:
        print("FAIL: Some scores are out of range.")
        
except Exception as e:
    print(f"IMPORT/EXECUTION FAILED: {e}")
