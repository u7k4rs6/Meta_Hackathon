from pydantic import BaseModel
from typing import Optional, List

class Action(BaseModel):
    action_type: str
    line_number: Optional[int] = None
    bug_type: Optional[str] = None
    fix_code: Optional[str] = None

class Observation(BaseModel):
    task_id: str
    diff_content: str
    flagged_line: Optional[int] = None
    goal: str
    step: int

    def to_prompt(self) -> str:
        prompt = f"Task: {self.task_id}\nGoal: {self.goal}\nStep: {self.step}\n\nDiff Content:\n{self.diff_content}\n"
        if self.flagged_line is not None:
            prompt += f"\nNote: A bug was found on line {self.flagged_line}. Please provide a fix.\n"
        return prompt

class Reward(BaseModel):
    score: float
    feedback: str

class State(BaseModel):
    task_id: str
    current_step: int
    done: bool
    history: List[str] = []
