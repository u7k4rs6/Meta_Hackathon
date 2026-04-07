from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os

from server.environment import Environment
from server.models import Action, Observation, State

app = FastAPI()
env = Environment()

os.makedirs("ui", exist_ok=True)
app.mount("/ui", StaticFiles(directory="ui"), name="ui")

class ResetRequest(BaseModel):
    task_id: str = "task1_easy"

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

@app.get("/")
def read_root():
    with open("ui/index.html", "r") as f:
        return HTMLResponse(content=f.read())
