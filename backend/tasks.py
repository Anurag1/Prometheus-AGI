import os
from celery import Celery
from prometheus_agi.agent import PrometheusAgent
from prometheus_agi.memory import KnowledgeGraphManager

# Configure Celery to use Redis as the message broker
celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")

@celery.task(name="run_agent_task")
def run_agent_task(project_name: str, project_goal: str):
    """The Celery task that runs the AGI in the background."""
    print(f"Celery worker received task for project: {project_name}")
    try:
        agent = PrometheusAgent(project_name=project_name, project_goal=project_goal)
        agent.run()
        return {"status": "Complete", "project": project_name}
    except Exception as e:
        return {"status": "Failed", "error": str(e)}

def get_project_status_and_data(project_name: str):
    """Helper function to read the latest knowledge graph for a project."""
    manager = KnowledgeGraphManager("workspace", project_name)
    kg = manager.load_kg()
    return kg