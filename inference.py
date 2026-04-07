import os
import sys
import json
import time
from openai import OpenAI
from client import CodeReviewEnv, CodeReviewAction

# Required env vars per spec
API_BASE_URL = os.environ.get("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME   = os.environ.get("MODEL_NAME", "gpt-4o-mini")
HF_TOKEN     = os.environ.get("HF_TOKEN", "")
ENV_URL      = os.environ.get("ENV_URL", "http://localhost:7860")

client = OpenAI(api_key=HF_TOKEN, base_url=API_BASE_URL)

SYSTEM_PROMPT = """You are a code reviewer. You will see a unified diff.
Reply with exactly one action in this format:
- To flag a bug: click_line(<line_number>, <bug_type>)
- To submit a fix: submit_fix(<line_number>, <fix_code>)
- If unsure: noop()
Bug types: off-by-one, null-deref, wrong-operator, missing-return
Only reply with the action, nothing else."""

TASKS = ["task1_easy", "task2_medium", "task3_hard"]

def log(tag, obj):
    print(f"{tag} {json.dumps(obj)}", flush=True)

env = CodeReviewEnv(base_url=ENV_URL).sync()

all_scores = []

log("[START]", {"tasks": TASKS, "model": MODEL_NAME, "base_url": API_BASE_URL})

for task_id in TASKS:
    try:
        obs = env.reset(task_id=task_id)
    except Exception as e:
        log("[STEP]", {"task": task_id, "step": 0, "action": "noop", "error": str(e)})
        all_scores.append(0.0)
        continue

    done  = False
    step  = 0
    score = 0.0
    result = None

    while not done:
        step += 1
        try:
            response = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user",   "content": obs.to_prompt()},
                ],
                max_tokens=100,
                temperature=0.0,
            )
            raw = response.choices[0].message.content.strip()
        except Exception:
            raw = "noop()"

        action = CodeReviewAction.from_text(raw)
        log("[STEP]", {"task": task_id, "step": step, "action": raw})

        try:
            result = env.step(action)
            obs, done = result.observation, result.done
            score = result.reward.score
        except Exception as e:
            log("[STEP]", {"task": task_id, "step": step, "error": str(e)})
            done = True

    all_scores.append(score)
    log("[END]", {"task": task_id, "score": score, "steps": step})

mean = sum(all_scores) / len(all_scores) if all_scores else 0.0
log("[END]", {"mean_score": mean, "scores": dict(zip(TASKS, all_scores))})
