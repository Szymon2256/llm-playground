import json
from services.llm_client import LLMClient

class PlannerAgent:
    def __init__(self):
        self.llm = LLMClient()

    def run(self, base_recipe: str) -> dict:
        prompt = (
            f"Create a detailed cooking recipe for the meal: '{base_recipe}'.\n"
            "Return a JSON object with EXACTLY this structure:\n"
            "- title (string)\n"
            "- ingredients (list of strings)\n"
            "- steps (list of objects with 'step_number' as int and 'instruction' as string)\n"
            "Respond ONLY with valid JSON."
        )
        response_str = self.llm.call_model_json(prompt)
        return json.loads(response_str)