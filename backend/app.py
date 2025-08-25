from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import os
from tasks import run_agent_task, get_project_status_and_data

app = FastAPI()

class Project(BaseModel):
    name: str
    goal: str

@app.post("/api/projects")
def create_project(project: Project):
    project_dir = os.path.join("workspace", project.name)
    if os.path.exists(project_dir):
        raise HTTPException(status_code=400, detail="Project already exists")
    os.makedirs(project_dir)
    return {"status": "Project created", "project_name": project.name}

@app.get("/api/projects")
def list_projects():
    if not os.path.exists("workspace"): return []
    return [d for d in os.listdir("workspace") if os.path.isdir(os.path.join("workspace", d))]

@app.get("/api/projects/{project_name}")
def get_project_details(project_name: str):
    if not os.path.exists(os.path.join("workspace", project_name)):
        raise HTTPException(status_code=404, detail="Project not found")
    return get_project_status_and_data(project_name)

@app.post("/api/projects/{project_name}/run")
def run_project_agent(project: Project):
    run_agent_task.delay(project_name=project.name, project_goal=project.goal)
    return {"status": "Agent run triggered in the background", "project_name": project.name}

app.mount("/static", StaticFiles(directory="../frontend"), name="static")

@app.get("/")
async def read_index():
    return FileResponse('../frontend/index.html')