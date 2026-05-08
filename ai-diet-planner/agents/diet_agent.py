import json
from services.llm_client import LLMClient

class DietAgent:
    def __init__(self):
        self.llm = LLMClient()

    def run(self, items: list, diet: str) -> dict:
        prompt = (
            f"Given these ingredients: {items} and the diet: {diet}.\n"
            "Return a JSON object with:\n"
            "compatible_items: list of ingredients from the input that fit the diet,\n"
            "suggested_recipe_ideas: exactly 5 recipe names that can be made.\n"
            "Respond ONLY with valid JSON."
        )
        response_str = self.llm.call_model_json(prompt)
        return json.loads(response_str)