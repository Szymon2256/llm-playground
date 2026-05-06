from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import FewShotPromptTemplate
from langchain_groq import ChatGroq
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage
import dotenv

dotenv.load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.5, max_retries=2)

# RAG builder
loader = DirectoryLoader('./planets', glob='**/*.txt', loader_cls=TextLoader)
documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=250, chunk_overlap=50)
docs = text_splitter.split_documents(documents)

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma.from_documents(docs, embeddings)

system_prompt = SystemMessage(content="You are a helpful assistant that uses tools to answer questions about planets.")

@tool("PlanetDistanceSun")
def PlanetDistanceSun(planet_name: str) -> str:
     """Take the name of a planet as input (string) and return its approximate distance from the Sun in Astronomical Units (AU)."""
     if "earth" in planet_name.lower():
        return "Earth is approximately 1 AU from the Sun."
     elif "mars" in planet_name.lower():
        return "Mars is approximately 1.5 AU from the Sun."
     elif "jupiter" in planet_name.lower():
        return "Jupiter is approximately 5.2 AU from the Sun."
     elif "pluto" in planet_name.lower():
        return "Pluto is approximately 39.5 AU from the Sun."
     else:
        return f"Information about the distance of {planet_name} from the Sun is not available in this tool."

@tool("PlanetRevolutionPeriod")
def PlanetRevolutionPeriod(planet_name: str) -> str:
     """Take the name of a planet as input (string) and return its approximate revolution period around the Sun in Earth years."""
     if "earth" in planet_name.lower():
        return "Earth takes approximately 1 Earth year to revolve around the Sun."
     elif "mars" in planet_name.lower():
        return "Mars takes approximately 1.88 Earth years to revolve around the Sun."
     elif "jupiter" in planet_name.lower():
        return "Jupiter takes approximately 11.86 Earth years to revolve around the Sun."
     elif "pluto" in planet_name.lower():
        return "Pluto takes approximately 248 Earth years to revolve around the Sun."
     else:
        return f"Information about the revolution period of {planet_name} is not available in this tool."

@tool("PlanetGeneralInfo")
def PlanetGeneralInfo(query: str) -> str:
     """Take the name of a planet or query with name of a planet as input (string) and handle general planet queries that are not about the planet's distance from the Sun or its revolution period."""
     answer = db.similarity_search(query)
     if answer:
        return answer[0].page_content
     else:
        return f"Additional information for {query} is not available in this tool."

tools_list = [PlanetDistanceSun, PlanetRevolutionPeriod, PlanetGeneralInfo]
tools_map = {tool.name: tool for tool in tools_list}

model_with_tools = llm.bind_tools(tools_list)

user_query = input()
messages = [system_prompt, HumanMessage(content=user_query)]
identified_tools = model_with_tools.invoke(messages)

if identified_tools.tool_calls:
     for tool in identified_tools.tool_calls:
         selected_tool = tools_map[tool["name"]]
         tool_output = selected_tool.invoke(tool)
         print(tool_output.content)
         print(identified_tools.tool_calls)
else:
     print(identified_tools.content)
     print(identified_tools.tool_calls)