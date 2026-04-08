import os
from server.models import Observation, Action, Reward
from server.graders.grader3 import grade_task3


class Task3Hard:
    def __init__(self):
        self.task_id = "task3_hard"
        self.goal = (
            "This diff introduces multiple bugs in an authentication service. "
            "Identify the primary bug (wrong dictionary key causing a KeyError) "
            "by reporting the line number and bug type, or submit a fix."
        )
        with open(os.path.join("diffs", "task3_hard.diff"), "r") as f:
            self.diff_content = f.read()
        self.current_step = 0
        self.max_steps = 5

    def reset(self):
        self.current_step = 0
        return self._get_obs()

    def _get_obs(self):
        return Observation(
            task_id=self.task_id,
            diff_content=self.diff_content,
            flagged_line=11,
            goal=self.goal,
            step=self.current_step,
        )

    def step(self, action: Action):
        self.current_step += 1
        done = False

        if action.action_type in ("click_line", "submit_fix"):
            score, feedback = grade_task3(action)
            done = True
        elif action.action_type == "noop":
            score = 0.05
            feedback = "No operation performed."
        else:
            score = 0.05
            feedback = "Invalid action."

        if self.current_step >= self.max_steps:
            done = True

        return self._get_obs(), Reward(score=score, feedback=feedback), done
