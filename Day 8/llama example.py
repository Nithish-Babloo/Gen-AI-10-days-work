First we need to create a folder named data -> upload a pdf file 


from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import Settings

# 1. Use local Llama as brain
Settings.llm = Ollama(model="llama3.2:1b", request_timeout=120.0)
Settings.embed_model = OllamaEmbedding(model_name="nomic-embed-text")

# 2. Read your documents from "data" folder
documents = SimpleDirectoryReader("data").load_data()

# 3. Make it searchable
index = VectorStoreIndex.from_documents(documents)

# 4. Ask question
query_engine = index.as_query_engine()
while True:
    q = input("what you observed?")
    if q.lower() == "exit":
        break
    print(query_engine.query(q))
