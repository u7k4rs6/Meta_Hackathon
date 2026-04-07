import os
from server.models import Observation, Action, Reward
from server.graders.grader1 import grade_task1

class Task1Easy:
    def __init__(self):
        self.task_id = "task1_easy"
        self.goal = "Find the off-by-one bug by reporting the line number and bug type."
        with open(os.path.join("diffs", "task1_easy.diff"), "r") as f:
            self.diff_content = f.read()
        self.target_line = 9  # The line number in our diff snippet
        self.target_bug_type = "off-by-one"
        self.current_step = 0
        self.max_steps = 5

    def reset(self):
        self.current_step = 0
        return self._get_obs()

    def _get_obs(self):
        return Observation(
            task_id=self.task_id,
            diff_content=self.diff_content,
            goal=self.goal,
            step=self.current_step
        )

    def step(self, action: Action):
        self.current_step += 1
        done = False
        
        if action.action_type == "click_line" and action.line_number is not None and action.bug_type is not None:
            score, feedback = grade_task1(action, self.target_line, self.target_bug_type)
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
