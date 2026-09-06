from langchain_text_splitters import SentenceTransformersTokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.retrievers import BM25Retriever
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from jinja2 import Environment, FileSystemLoader
from dotenv import load_dotenv
from langchain_chroma import Chroma
from pathlib import Path
import requests
import os

load_dotenv()
NVIDIA_EMBEDDINGS_URL = "https://integrate.api.nvidia.com/v1/embeddings"

env = Environment(loader=FileSystemLoader("."))
template = env.get_template("prompt.jinja")

API_KEY = os.getenv("NVIDIA_API_KEY")

class NvidiaEmbeddings(Embeddings):
    def __init__(self, api_key, url=NVIDIA_EMBEDDINGS_URL, model="nvidia/nemotron-3-embed-1b"):
        self.api_key = api_key
        self.url = url
        self.model = model

    def _embed(self, texts):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.model,
            "input": texts
        }
        response = requests.post(headers=headers, url=self.url, json=payload)
        data = response.json()
        return [item["embedding"] for item in data["data"]]

    def embed_documents(self, texts):
        # PDF chunks embed karne ke liye (add_texts ke waqt)
        return self._embed(texts)

    def embed_query(self, text):
        # User ki query embed karne ke liye (retriever.invoke ke waqt)
        return self._embed([text])[0]

def load_docs():
    docs = []
    pdf_folder = Path("to_do") / "Nova.ai_Policy"

    for pdf in pdf_folder.glob("*.pdf"):
        loader = PyPDFLoader(str(pdf))
        docs.extend(loader.load())

    return docs


def load_vectorstore(persist_dir="chroma_db"):
    embedding_fn = NvidiaEmbeddings(api_key=API_KEY)

    vector_store = Chroma(
        persist_directory=persist_dir,
        collection_name="nova_policy",
        embedding_function=embedding_fn   
    )

    existing = vector_store.get()
    if existing and len(existing["ids"]) > 0:
        print(f"Existing vectorstore mil gaya ({len(existing['ids'])} chunks), re-embedding skip kar rahe hain...")
        return vector_store

    # Sirf pehli baar (jab collection empty ho) ye chalega
    docs = load_docs()

    text_splitter = SentenceTransformersTokenTextSplitter(
        chunk_size=433,
        chunk_overlap=0
    )
    chunks = text_splitter.split_documents(docs)

    embeddings_list = embedding_fn.embed_documents(
        [chunk.page_content for chunk in chunks]
    )

    print(f"Chunks: {len(chunks)}, Embeddings: {len(embeddings_list)}")

    vector_store.add_texts(
        texts=[chunk.page_content for chunk in chunks],
        embeddings=embeddings_list,
        metadatas=[chunk.metadata for chunk in chunks]
    )

    return vector_store


def main(user_input: str) -> str:
    url = "https://integrate.api.nvidia.com/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    vec = load_vectorstore()
    retriever = vec.as_retriever(search_type="mmr", k=2)

    stored = vec.get()
    retriever_bm = BM25Retriever.from_documents(
        [Document(page_content=text, metadata=meta)
         for text, meta in zip(stored["documents"], stored["metadatas"])],
        k=2
    )

    results = retriever.invoke(user_input)
    results_bm = retriever_bm.invoke(user_input)
    context = "\n\n".join([doc.page_content for doc in results])
    context_bm = "\n\n".join([doc.page_content for doc in results_bm])

    prompt = template.render(user_query=user_input, context=context, context_bm=context_bm)
    payload = {
        "model": "nvidia/nemotron-3-super-120b-a12b",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }

    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    print("STATUS:", response.status_code)
    print("RESPONSE:", data)
    return data['choices'][0]['message']['content']


if __name__ == "__main__":
    while True:
        user_input = input("ask the query:- ")
        if user_input == "exit":
            print("Good Bye🫡")
            break
        print("\nAnswer:", main(user_input), "\n")