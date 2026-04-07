from server.models import Action, Observation, Reward, State
from server.tasks.task1 import Task1Easy
from server.tasks.task2 import Task2Medium
from server.tasks.task3 import Task3Hard

class Environment:
    def __init__(self):
        self.tasks = {
            "task1_easy": Task1Easy(),
            "task2_medium": Task2Medium(),
            "task3_hard": Task3Hard(),
        }
        self.current_task = None
        self.history = []

    def reset(self, task_id: str):
        if task_id not in self.tasks:
            raise ValueError(f"Unknown task {task_id}")
        self.current_task = self.tasks[task_id]
        self.history = []
        return self.current_task.reset()

    def step(self, action: Action):
        if not self.current_task:
            raise ValueError("Environment not reset")
        
        obs, reward, done = self.current_task.step(action)
        self.history.append(f"Action: {action.model_dump_json()}, Reward: {reward.model_dump_json()}, Done: {done}")
        
        return {
            "observation": obs,
            "reward": reward,
            "done": done,
            "info": {}
        }
    
    def get_state(self):
        if not self.current_task:
            return State(task_id="", current_step=0, done=True, history=[])
        return State(
            task_id=self.current_task.task_id,
            current_step=self.current_task.current_step,
            done=self.current_task.current_step >= self.current_task.max_steps,
            history=self.history
        )
