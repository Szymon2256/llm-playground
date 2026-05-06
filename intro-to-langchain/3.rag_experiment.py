from langchain_core.prompts import PromptTemplate
from langchain_core.prompts import FewShotPromptTemplate
from langchain_groq import ChatGroq
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

import dotenv

dotenv.load_dotenv()

llm = ChatGroq(model="llama-3.3-70b-versatile", temperature=0.5, max_retries=2)

loader = DirectoryLoader('./planets', glob='**/*.txt', loader_cls=TextLoader)
documents = loader.load()

text_splitter = CharacterTextSplitter(chunk_size=100, chunk_overlap=5)
docs = text_splitter.split_documents(documents)

embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
db = Chroma.from_documents(docs, embeddings)

question = input()
answer = db.similarity_search(question)
print(answer[0].page_content)