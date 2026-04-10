from pydantic import BaseModel, field_validator
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

    @field_validator("score")
    @classmethod
    def clamp_score(cls, v: float) -> float:
        """Ensure score is ALWAYS strictly between 0 and 1 (exclusive).
        This is the ultimate safety net — no matter what any grader returns,
        the score will never be exactly 0.0 or 1.0."""
        # Clamp to a safe range (0.05, 0.95) to stay far from boundaries
        clamped = max(0.05, min(0.95, float(v)))
        # Final absolute safety check returning pure float without rounding
        if clamped <= 0.0:
            clamped = 0.05
        if clamped >= 1.0:
            clamped = 0.95
        return float(clamped)


class State(BaseModel):
    task_id: str
    current_step: int
    done: bool
    history: List[str] = []
