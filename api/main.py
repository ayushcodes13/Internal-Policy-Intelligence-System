from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from api.pipeline import run_pipeline


app = FastAPI(title="CANON Policy Intelligence API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:3000",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://localhost:5173",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    query: str = Field(min_length=1, max_length=2000)


@app.get("/health")
def health() -> dict:
    return {"status": "ok", "service": "canon-python-api"}


@app.post("/api/query")
def query_policy(request: QueryRequest) -> dict:
    try:
        return run_pipeline(request.query)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
