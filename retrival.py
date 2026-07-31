from langchain_text_splitters import SentenceTransformersTokenTextSplitter
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv
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

def get_nvidia_embeddings():
    docs = load_docs()
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    text_splitter = SentenceTransformersTokenTextSplitter(
    chunk_size=433,
    chunk_overlap=0
    )

    chunks=text_splitter.split_documents(docs)

    print(f"Number of chunks created: {len(chunks)}")

    # Optional: inspect a sample chunk
    # if chunks:
        # print("Sample chunk content:\n", chunks[0].page_content[:300])
        # print("Sample chunk metadata:\n", chunks[0].metadata)

    embeddings = []
    payload = {
            "model": "nvidia/nv-embed-v1",
            "input": [chunk.page_content for chunk in chunks]
    }
    response = requests.post(headers=headers, url=NVIDIA_EMBEDDINGS_URL, json = payload)

    data = response.json()
    embedding = data["data"][0]["embedding"]
    print(len(embedding))

ret=get_nvidia_embeddings()
