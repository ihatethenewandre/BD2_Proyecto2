import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.db import db


@asynccontextmanager
async def lifespan(app: FastAPI):
    db.connect()
    yield
    db.close()


app = FastAPI(
    title="BD II - Proyecto #2 - Detección Fraude",
    description="Backend para Proyecto #2 de Neo4j",
    version="0.1.0",
    lifespan=lifespan,
)

cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[o.strip() for o in cors_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "proyecto": "BD II - Proyecto #2 - Detección Fraude",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health():
    try:
        result = db.run_query("RETURN 'pong' AS mensaje, datetime() AS hora")
        return {
            "status": "ok",
            "neo4j": result[0] if result else None,
        }
    except Exception as e:
        raise HTTPException(status_code=503, detail=f"Neo4j No Responde: {e}")