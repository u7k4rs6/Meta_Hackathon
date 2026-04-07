import os
from server.models import Observation, Action, Reward
from server.graders.grader2 import grade_task2

class Task2Medium:
    def __init__(self):
        self.task_id = "task2_medium"
        self.goal = "Provide the correct fix code for the flagged line."
        with open(os.path.join("diffs", "task2_medium.diff"), "r") as f:
            self.diff_content = f.read()
        self.target_line = 14  # Updated line number based on parser diff
        self.flagged_line = 14
        self.current_step = 0
        self.max_steps = 5

    def reset(self):
        self.current_step = 0
        return self._get_obs()

    def _get_obs(self):
        return Observation(
            task_id=self.task_id,
            diff_content=self.diff_content,
            flagged_line=self.flagged_line,
            goal=self.goal,
            step=self.current_step
        )

    def step(self, action: Action):
        self.current_step += 1
        done = False
        
        if action.action_type == "submit_fix" and action.line_number is not None and action.fix_code is not None:
            score, feedback = grade_task2(action, self.target_line)
            done = True
        elif action.action_type == "noop":
            score = 0.01
            feedback = "No operation performed."
        else:
            score = 0.05
            feedback = "Invalid action."

        if self.current_step >= self.max_steps:
            done = True

        return self._get_obs(), Reward(score=score, feedback=feedback), done
