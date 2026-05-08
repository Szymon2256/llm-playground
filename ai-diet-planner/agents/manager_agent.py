from agents.inventory_agent import InventoryAgent
from agents.diet_agent import DietAgent


class ManagerAgent:
    def __init__(self):
        self.inventory_agent = InventoryAgent()
        self.diet_agent = DietAgent()

    def run(self, items: list, diet: str) -> dict:
        # Krok 1: Filtrowanie ekwipunku
        inventory_result = self.inventory_agent.run(items)
        usable_items = inventory_result.get("usable_items", [])

        # Krok 2: Filtrowanie diety i przepisy (używamy tylko przefiltrowanych składników!)
        diet_result = self.diet_agent.run(usable_items, diet)

        # Krok 3: Zwrócenie połączonego wyniku w wymaganym formacie
        return {
            "usable_items": usable_items,
            "diet_filtered": diet_result.get("compatible_items", []),
            "suggestions": diet_result.get("suggested_recipe_ideas", [])
        }