import httpx
from pydantic import BaseModel
from typing import Optional, Any
from server.models import Action, Observation, Reward

class StepResult(BaseModel):
    observation: Observation
    reward: float
    done: bool
    info: dict

class CodeReviewAction:
    @staticmethod
    def from_text(text: str) -> Action:
        try:
            text = text.strip()
            if text.startswith("click_line("):
                content = text[len("click_line("):-1]
                parts = content.split(",", 1)
                line = int(parts[0].strip())
                bug_type = parts[1].strip().strip("'\"")
                return Action(action_type="click_line", line_number=line, bug_type=bug_type)
            elif text.startswith("submit_fix("):
                content = text[len("submit_fix("):-1]
                parts = content.split(",", 1)
                line = int(parts[0].strip())
                fix_code = parts[1].strip().strip("'\"")
                return Action(action_type="submit_fix", line_number=line, fix_code=fix_code)
            else:
                return Action(action_type="noop")
        except Exception:
            return Action(action_type="noop")

class CodeReviewEnvClient:
    def __init__(self, base_url: str):
        self.base_url = base_url.rstrip('/')
        self.client = httpx.Client()

    def reset(self, task_id: str) -> Observation:
        resp = self.client.post(f"{self.base_url}/reset", json={"task_id": task_id})
        resp.raise_for_status()
        return Observation(**resp.json())

    def step(self, action: Action) -> StepResult:
        resp = self.client.post(f"{self.base_url}/step", json=action.model_dump())
        resp.raise_for_status()
        return StepResult(**resp.json())

class CodeReviewEnv:
    def __init__(self, base_url: str):
        self.base_url = base_url
    
    def sync(self):
        return CodeReviewEnvClient(self.base_url)
