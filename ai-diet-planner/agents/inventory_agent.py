import json
from services.llm_client import LLMClient

class InventoryAgent:
    def __init__(self):
        self.llm = LLMClient()

    def run(self, items: list) -> dict:
        prompt = (
            f"You are a kitchen assistant. Given the JSON array of ingredients:\n{items}\n"
            "Return a JSON object with:\n"
            "usable_items: an array of ingredients that are non-empty and suitable for cooking,\n"
            "message: a short confirmation string.\n"
            "Respond ONLY with valid JSON."
        )
        response_str = self.llm.call_model_json(prompt)
        return json.loads(response_str)