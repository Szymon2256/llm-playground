from pydantic import BaseModel
from typing import List

# Struktury dla pojedynczego przepisu
class RecipeStep(BaseModel):
    step_number: int
    instruction: str

class RecipeResponse(BaseModel):
    title: str
    ingredients: List[str]
    steps: List[RecipeStep]

class PlanInput(BaseModel):
    base_recipe: str

# Struktury dla rekomendacji (łączenie wszystkiego)
class RecommendInput(BaseModel):
    items: List[str]
    diet: str
    recipe_count: int

class RecommendResponse(BaseModel):
    recipes: List[RecipeResponse]