from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq
import dotenv

dotenv.load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.5, max_retries=2)

question = input()
template = PromptTemplate.from_template("You are a helpful assistant who answers questions users may have. You are asked: {question}.")

prompt = template.invoke({"question": question})
response = llm.invoke(prompt)
print(response.content)