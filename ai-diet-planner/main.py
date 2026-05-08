from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from agents.inventory_agent import InventoryAgent
from agents.diet_agent import DietAgent
from agents.manager_agent import ManagerAgent
from models import PlanInput, RecipeResponse, RecommendInput, RecommendResponse
from agents.planner_agent import PlannerAgent
from logging_config import get_logger # używamy nowej nazwy pliku

logger = get_logger("app")

app = FastAPI(title="AI Diet & Meal Planner")

# Modele Pydantic
class InventoryInput(BaseModel):
    items: List[str]

class InventoryResponse(BaseModel):
    usable_items: List[str]
    message: str

class DietInput(BaseModel):
    items: List[str]
    diet: str

class DietResponse(BaseModel):
    compatible_items: List[str]
    suggested_recipe_ideas: List[str]

class AskInput(BaseModel):
    items: List[str]
    diet: str

class AskResponse(BaseModel):
    usable_items: List[str]
    diet_filtered: List[str]
    suggestions: List[str]

# Endpointy
@app.get("/")
async def root():
    return {"message": "Success!"}

@app.post("/inventory", response_model=InventoryResponse)
async def process_inventory(data: InventoryInput):
    agent = InventoryAgent()
    result = agent.run(data.items)
    return result

@app.post("/diet", response_model=DietResponse)
async def process_diet(data: DietInput):
    agent = DietAgent()
    result = agent.run(data.items, data.diet)
    return result

@app.post("/ask", response_model=AskResponse)
async def process_ask(data: AskInput):
    logger.info("Received /ask request: items=%s, diet=%s", data.items, data.diet)
    manager = ManagerAgent()
    result = manager.run(data.items, data.diet)
    logger.info("/ask response: suggestions=%s", result["suggestions"])
    return result


@app.post("/plan", response_model=RecipeResponse)
async def create_plan(data: PlanInput):
    logger.info("Received /plan request: base_recipe=%s", data.base_recipe)
    planner = PlannerAgent()
    result = planner.run(data.base_recipe)
    logger.info("/plan response: title=%s", result["title"])
    return result


@app.post("/recommend", response_model=RecommendResponse)
async def recommend_recipes(data: RecommendInput):
    logger.info("Received /recommend request: items=%s, diet=%s, count=%d",
                data.items, data.diet, data.recipe_count)
    # 1. Wywołujemy Managera (który uruchomi Inventory i Diet Agent)
    manager = ManagerAgent()
    ask_result = manager.run(data.items, data.diet)

    # 2. Pobieramy sugestie i obcinamy je do limitu (recipe_count)
    suggestions = ask_result.get("suggestions", [])
    selected_suggestions = suggestions[:data.recipe_count]

    # 3. Odpytujemy PlannerAgent o szczegółowy przepis dla każdej sugestii
    planner = PlannerAgent()
    recipes = []
    for meal_name in selected_suggestions:
        recipe_details = planner.run(meal_name)
        recipes.append(recipe_details)

    logger.info("/recommend response: generated %d recipes", len(recipes))
    # Zwracamy gotową listę wygenerowanych przepisów
    return {"recipes": recipes}