# CodeReview OpenEnv Environment

An OpenEnv-compliant environment for a Meta x PyTorch hackathon where an AI agent naviages a Code Review Dashboard web UI, reads unified diffs, and takes structured actions (flagging bugs, submitting fixes).

## Architecture

- **`server/app.py`**: FastAPI application serving the state machine endpoints and the static UI.
- **`ui/`**: HTML/JS/CSS frontend built without frameworks.
- **`client.py`**: Client wrapper to easily interact with the environment from inference scripts.
- **`inference.py`**: An example agent interacting with the environment using the OpenAI client.
