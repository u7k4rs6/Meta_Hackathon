import os
from openai import OpenAI
from client import CodeReviewEnv, CodeReviewAction

API_BASE_URL = os.environ.get("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.environ.get("MODEL_NAME", "gpt-3.5-turbo")
HF_TOKEN = os.environ.get("HF_TOKEN", "")

client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)

SYSTEM_PROMPT = """
You are a code reviewer. You will see a unified diff.
Reply with exactly one action in this format:
- To flag a bug: click_line(<line_number>, <bug_type>)
- To submit a fix: submit_fix(<line_number>, <fix_code>)
- If unsure: noop()
Bug types: off-by-one, null-deref, wrong-operator, missing-return
"""

TASKS = ["task1_easy", "task2_medium"]
scores = []

env = CodeReviewEnv(base_url=os.getenv("ENV_URL", "http://localhost:7860")).sync()

for task_id in TASKS:
    obs = env.reset(task_id=task_id)
    done = False
    result = None
    while not done:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": obs.to_prompt()}
            ],
            max_tokens=100,
            temperature=0.0,
        )
        raw = completion.choices[0].message.content or "noop()"
        action = CodeReviewAction.from_text(raw)
        result = env.step(action)
        obs, done = result.observation, result.done
    
    score = result.reward.score if result else 0.0
    scores.append(score)
    print(f"{task_id}: {score:.3f}")

if scores:
    print(f"Mean: {sum(scores)/len(scores):.3f}")
else:
    print("Mean: 0.000")
