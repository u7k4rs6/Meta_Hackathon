from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import sys

# Ensure the parent directory is in the path for absolute imports like 'from server.xxx'
# This is critical for the platform entrypoint to resolve the 'server' package.
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from server.environment import Environment
from server.models import Action, Observation, State
from server.graders.grader1 import grade as grade1
from server.graders.grader2 import grade as grade2
from server.graders.grader3 import grade as grade3

app = FastAPI()
env = Environment()

GRADERS = {
    "task1_easy": grade1,
    "task2_medium": grade2,
    "task3_hard": grade3,
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UI_DIR = os.path.join(BASE_DIR, "ui")

os.makedirs(UI_DIR, exist_ok=True)
app.mount("/ui", StaticFiles(directory=UI_DIR), name="ui")

class ResetRequest(BaseModel):
    task_id: str = "task1_easy"

class GradeRequest(BaseModel):
    action_type: str = "noop"
    line_number: int | None = None
    bug_type: str | None = None
    fix_code: str | None = None

@app.post("/reset", response_model=Observation)
def reset(request: ResetRequest = ResetRequest()):
    try:
        obs = env.reset(request.task_id)
        return obs
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/step")
def step(action: Action):
    try:
        return env.step(action)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/state", response_model=State)
def state():
    return env.get_state()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/grade/{task_id}")
def grade(task_id: str, request: GradeRequest = GradeRequest()):
    """Grade an action for a specific task. Returns score strictly in (0, 1)."""
    if task_id not in GRADERS:
        raise HTTPException(status_code=404, detail=f"Unknown task: {task_id}")
    grader_fn = GRADERS[task_id]
    action_data = request.model_dump()
    score = grader_fn(action_data)
    return {"task_id": task_id, "score": float(score), "reward": float(score)}

@app.get("/")
def read_root():
    index_path = os.path.join(UI_DIR, "index.html")
    with open(index_path, "r") as f:
        return HTMLResponse(content=f.read())

def main():
    import uvicorn
    uvicorn.run("server.app:app", host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()

