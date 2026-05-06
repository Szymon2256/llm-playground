from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import FewShotPromptTemplate
from langchain_groq import ChatGroq
import dotenv

dotenv.load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.5, max_retries=2)

question = input()
examples = [
    {"input": "Jupiter", "output": "Jupiter is the largest planet in the solar system. It is a gas giant primarily composed of hydrogen and helium. It has a Great Red Spot, a massive storm, and at least 79 known moons, including Ganymede, the largest moon in the solar system."},
    {"input": "Mars", "output": "Mars is the fourth planet from the Sun. It has a thin atmosphere composed mainly of carbon dioxide and is known for its red appearance due to iron oxide on its surface. Notable features include Olympus Mons, the largest volcano in the solar system, and Valles Marineris, a vast canyon system."},
]

example_template = PromptTemplate.from_template("Q: What is a {input}? Provide essential details such as: Physical characteristics (size, composition, atmosphere), Notable features (rings, moons, surface conditions), Scientific or historical significance and Fun or surprising facts about {input}.\nA: {output}")

few_shot_prompt = FewShotPromptTemplate(
    examples=examples,
    example_prompt=example_template,
    suffix="Q: What is a {question}? Provide essential details such as: Physical characteristics (size, composition, atmosphere), Notable features (rings, moons, surface conditions), Scientific or historical significance and Fun or surprising facts about {question}.\nA:",
    input_variables=["question"],
)

final_prompt = few_shot_prompt.format(question=question)

response = llm.invoke(final_prompt)

print(response.content)