from .memory import KnowledgeGraphManager
from .metamind import MetaMind
from .toolkit.data_tools import StockPriceFetcher
from .toolkit.web_tools import WebScraper

class PrometheusAgent:
    def __init__(self, project_name: str, project_goal: str):
        self.project_name = project_name
        self.goal = project_goal
        self.memory = KnowledgeGraphManager("workspace", self.project_name)
        self.metamind = MetaMind()
        self.tools = {
            "stock_price_fetcher": StockPriceFetcher(),
            "web_scraper": WebScraper(),
        }

    def _execute_plan(self, plan: list[dict]) -> dict:
        state = {}
        print("\n[AGENT] Executing state gathering plan...")
        for step in plan:
            tool_name, args = step.get("tool_name"), step.get("args", {})
            if tool_name in self.tools:
                result = self.tools[tool_name].run(**args)
                state[f"{tool_name}_{list(args.values())[0]}"] = result
        return state

    def _compare_states(self, old_state: dict, new_state: dict) -> dict:
        changes = {}
        all_keys = set(old_state.keys()) | set(new_state.keys())
        for key in all_keys:
            if old_state.get(key) != new_state.get(key):
                changes[key] = {"from": old_state.get(key), "to": new_state.get(key)}
        return changes

    def run(self):
        print("="*60)
        print(f"Prometheus Agent RUNNING for Project: {self.project_name}")
        previous_state = self.memory.get_latest_state()
        plan = self.metamind.plan_state_gathering(self.goal, list(self.tools.keys()))
        current_state = self._execute_plan(plan)
        changes = self._compare_states(previous_state, current_state)
        hypotheses = self.metamind.analyze_and_hypothesize(self.goal, changes)
        self.memory.save_run(current_state, hypotheses)
        print("="*60)