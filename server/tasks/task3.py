import os
from server.models import Observation, Action, Reward
from server.graders.grader3 import grade_task3

class Task3Hard:
    def __init__(self):
        self.task_id = "task3_hard"
        self.goal = "Identify the wrong-operator bug in the validator logic."
        with open(os.path.join("diffs", "task3_hard.diff"), "r") as f:
            self.diff_content = f.read()
        self.target_line = 10  # line with wrong operator: > 0 vs == 0
        self.target_bug_type = "wrong-operator"
        self.current_step = 0
        self.max_steps = 5

    def reset(self):
        self.current_step = 0
        return self._get_obs()

    def _get_obs(self):
        return Observation(
            task_id=self.task_id,
            diff_content=self.diff_content,
            flagged_line=None,
            goal=self.goal,
            step=self.current_step
        )

    def step(self, action: Action):
        self.current_step += 1
        done = False

        if action.action_type == "click_line" and action.line_number is not None:
            score, feedback = grade_task3(action, self.target_line, self.target_bug_type)
            done = True
        elif action.action_type == "noop":
            score = 0.01
            feedback = "No operation performed."
        else:
            score = 0.01
            feedback = "Invalid action for this task."

        if self.current_step >= self.max_steps:
            done = True

        return self._get_obs(), Reward(score=score, feedback=feedback), done
