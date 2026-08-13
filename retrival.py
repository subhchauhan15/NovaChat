from langchain_text_splitters import SentenceTransformersTokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv
from langchain_chroma import Chroma
from pathlib import Path
import requests
import os
# from lagchain_chroma

load_dotenv()
NVIDIA_EMBEDDINGS_URL="https://integrate.api.nvidia.com/v1/embeddings"

API_KEY=os.getenv("NVIDIA_API_KEY")
# print(API_KEY)
def load_docs():
    docs = []

    pdf_folder = Path("to_do") / "Nova.ai_Policy"

    for pdf in pdf_folder.glob("*.pdf"):
        loader = PyPDFLoader(str(pdf))
        docs.extend(loader.load())

    return docs

def load_vectorstore(persist_dir="chroma_db"):
    docs = load_docs()

    text_splitter = SentenceTransformersTokenTextSplitter(
        chunk_size=433,
        chunk_overlap=0
    )
    chunks = text_splitter.split_documents(docs)

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "nvidia/nv-embed-v1",
        "input": [chunk.page_content for chunk in chunks]
    }
    response = requests.post(headers=headers, url=NVIDIA_EMBEDDINGS_URL, json=payload)
    data = response.json()

    embeddings_list = [item["embedding"] for item in data["data"]]

    print(f"Chunks: {len(chunks)}, Embeddings: {len(embeddings_list)}")  

    vector_store = Chroma(
        persist_directory=persist_dir,
        collection_name="nova_policy"
    )

    vector_store.add_texts(
        texts=[chunk.page_content for chunk in chunks],
        embeddings=embeddings_list,
        metadatas=[chunk.metadata for chunk in chunks]
    )
    print("TEXT:", chunks[0].page_content[:300])
    print("METADATA:", chunks[0].metadata)
    print("EMBEDDING (first 5 values):", embeddings_list[0][:5])
    print("EMBEDDING LENGTH:", len(embeddings_list[0]))
    return vector_store

z=load_vectorstore()