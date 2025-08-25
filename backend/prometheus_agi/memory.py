import os
import json

class KnowledgeGraphManager:
    def __init__(self, workspace_dir: str, project_name: str):
        self.project_dir = os.path.join(workspace_dir, project_name)
        self.kg_file = os.path.join(self.project_dir, "knowledge_graph.json")
        os.makedirs(self.project_dir, exist_ok=True)

    def load_kg(self) -> dict:
        try:
            with open(self.kg_file, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"latest_state": {}, "hypotheses": {}}

    def get_latest_state(self) -> dict:
        return self.load_kg().get("latest_state", {})

    def save_run(self, state: dict, hypotheses: list):
        kg = self.load_kg()
        kg["latest_state"] = state
        for h in hypotheses:
            if h['id'] not in kg["hypotheses"]:
                kg["hypotheses"][h['id']] = h
        with open(self.kg_file, 'w') as f:
            json.dump(kg, f, indent=2)
        print(f"\n[MEMORY] Saved state and hypotheses to {self.kg_file}")