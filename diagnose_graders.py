import sys
import os

# Add root to sys.path
sys.path.append(os.getcwd())

def diagnose():
    tasks = ["grader1", "grader2", "grader3"]
    
    for t in tasks:
        print(f"--- Diagnosing {t} ---")
        try:
            # Dynamic import
            module = __import__(f"server.graders.{t}", fromlist=["grade"])
            grade_fn = getattr(module, "grade")
            
            # Test with dummy data
            dummy_data = {
                "action_type": "noop",
                "line_number": 1,
                "bug_type": "none",
                "fix_code": ""
            }
            
            score = grade_fn(dummy_data)
            print(f"Resulting score: {score}")
            
            if 0.0 < score < 1.0:
                print("PASSED: Score is in strict (0, 1) range.")
            else:
                print(f"FAILED: Score {score} is OUTSIDE (0, 1) range.")
                
            if isinstance(score, float):
                print("PASSED: Type is float.")
            else:
                print(f"FAILED: Type is {type(score)}, expected float.")
                
        except Exception as e:
            print(f"ERROR diagnosing {t}: {e}")
            import traceback
            traceback.print_exc()
        print()

if __name__ == "__main__":
    diagnose()
