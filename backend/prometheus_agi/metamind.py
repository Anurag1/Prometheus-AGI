import ollama
import json

class MetaMind:
    LLM_MODEL = "llama3"

    def plan_state_gathering(self, project_goal: str, available_tools: list[str]) -> list[dict]:
        print("\n[META-MIND] Generating plan to establish baseline state...")
        system_prompt = f"""
You are the Planner Core for an AGI. The AGI's high-level goal is: '{project_goal}'
Create a step-by-step plan to gather data for this goal using the provided tools.
Your response must be a JSON object with a "plan" key, which is a list of tool calls.
Each tool call object must have "tool_name" and "args" (a dictionary).
"""
        user_prompt = f"Available tools: {json.dumps(available_tools)}"
        response = ollama.chat(model=self.LLM_MODEL, format="json", messages=[
            {'role': 'system', 'content': system_prompt}, {'role': 'user', 'content': user_prompt}
        ])
        return json.loads(response['message']['content']).get("plan", [])

    def analyze_and_hypothesize(self, project_goal: str, changes: dict) -> list:
        if not changes: return []
        print("\n[META-MIND] Analyzing changes and generating hypotheses...")
        system_prompt = f"""
You are the Analyst & Theorist Core for an AGI. The AGI's goal is: '{project_goal}'
Analyze the following detected changes. Generate a set of testable, high-value hypotheses relevant to the goal.
Your response MUST be a JSON object with a "hypotheses" key, a list of objects.
Each hypothesis must have "id", "priority", and "description".
"""
        user_prompt = f"Detected Changes:\n{json.dumps(changes, indent=2)}"
        response = ollama.chat(model=self.LLM_MODEL, format="json", messages=[
            {'role': 'system', 'content': system_prompt}, {'role': 'user', 'content': user_prompt}
        ])
        return json.loads(response['message']['content']).get("hypotheses", [])