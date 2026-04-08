import os
from dotenv import load_dotenv
load_dotenv()
from google import genai
from google.genai import types
from client import CodeReviewEnv, CodeReviewAction

MODEL_NAME = os.environ.get("MODEL_NAME", "gemini-1.5-pro")
# We lookup GEMINI_API_KEY or fallback to GEMINI since it's commonly used
API_KEY = os.environ.get("GEMINI_API_KEY", os.environ.get("GEMINI", ""))

client = genai.Client(api_key=API_KEY)

SYSTEM_PROMPT = """
You are a code reviewer. You will see a unified diff.
Reply with exactly one action in this format:
- To flag a bug: click_line(<line_number>, <bug_type>)
- To submit a fix: submit_fix(<line_number>, <fix_code>)
- If unsure: noop()
Bug types: off-by-one, null-deref, wrong-operator, missing-return
"""

TASKS = ["task1_easy", "task2_medium", "task3_hard"]
scores = []

env = CodeReviewEnv(base_url=os.getenv("ENV_URL", "http://localhost:7860")).sync()

for task_id in TASKS:
    obs = env.reset(task_id=task_id)
    done = False
    result = None
    while not done:
        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=obs.to_prompt(),
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    max_output_tokens=100,
                    temperature=0.0,
                )
            )
            raw = response.text
        except Exception:
            raw = "noop()"
        action = CodeReviewAction.from_text(raw)
        result = env.step(action)
        obs, done = result.observation, result.done
    
    score = result.reward.score if result else 0.05
    # Clamp score to be strictly within (0, 1) as required by the validator
    score = max(0.01, min(0.99, score))
    scores.append(score)
    print(f"{task_id}: {score:.3f}")

if scores:
    print(f"Mean: {sum(scores)/len(scores):.3f}")
else:
    print("Mean: 0.000")
