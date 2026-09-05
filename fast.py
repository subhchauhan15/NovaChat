from fastapi import FastAPI
from pydantic import BaseModel
from retrival import main
import uvicorn

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

@app.post("/chat")
def chat(request: QueryRequest):
    answer = main(request.query)
    return {"query": request.query, "answer": answer}

if __name__ == "__main__":
    uvicorn.run("fast:app", host="0.0.0.0", port=8000, reload=True)