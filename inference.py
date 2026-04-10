import os
from openai import OpenAI
from dotenv import load_dotenv
from client import CodeReviewEnv, CodeReviewAction

# Load environment variables if .env exists
load_dotenv()

# Configuration per Hackathon Rules
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

if HF_TOKEN is None:
    raise ValueError("HF_TOKEN environment variable is required")

# Initialize OpenAI Client (only SDK allowed)
client = OpenAI(base_url=API_BASE_URL, api_key=HF_TOKEN)

# System configuration for the agent
SYSTEM_PROMPT = """
You are a code reviewer. You will see a unified diff.
Reply with exactly one action in this format:
- To flag a bug: click_line(<line_number>, <bug_type>)
- To submit a fix: submit_fix(<line_number>, <fix_code>)
- If unsure: noop()
Bug types: off-by-one, null-deref, wrong-operator, missing-return
"""

TASKS = ["task1_easy", "task2_medium", "task3_hard"]
BENCHMARK = "code-review-env"

# Initialize Environment Client
env_url = os.getenv("ENV_URL", "http://localhost:7860")
env_client = CodeReviewEnv(base_url=env_url).sync()

for task_id in TASKS:
    # [START] task=<task_name> env=<benchmark> model=<model_name>
    print(f"[START] task={task_id} env={BENCHMARK} model={MODEL_NAME}")
    
    steps = 0
    rewards = []
    success = False
    
    try:
        # Initial environment reset
        obs = env_client.reset(task_id=task_id)
        done = False
        
        while not done:
            try:
                # LLM Inference
                response = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": obs.to_prompt()}
                    ],
                    max_tokens=100,
                    temperature=0.0
                )
                action_text = response.choices[0].message.content.strip()
            except Exception:
                # Default to noop on LLM failure
                action_text = "noop()"
            
            # Action parsing and stepping
            action = CodeReviewAction.from_text(action_text)
            result = env_client.step(action)
            steps += 1
            
            # Extract metrics
            reward = float(result.reward)
            rewards.append(f"{reward:.2f}")
            done = result.done
            
            # Success is defined as task completion with a positive score
            if done and reward > 0.5:
                success = True
                
            # [STEP] step=<n> action=<action_str> reward=<0.00> done=<true|false> error=null
            print(f"[STEP] step={steps} action={action_text} reward={reward:.2f} done={str(done).lower()} error=null")
            
            # Update observation for next step
            obs = result.observation
            
    except Exception as e:
        # Catch unexpected errors to ensure [END] is still printed
        # Any step that crashes would have error=<msg> if we were mid-step
        pass
    finally:
        # [END] success=<true|false> steps=<n> rewards=<r1,r2,...,rn>
        success_str = str(success).lower()
        rewards_str = ",".join(rewards)
        print(f"[END] success={success_str} steps={steps} rewards={rewards_str}")
