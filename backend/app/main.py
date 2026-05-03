import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.forest import fraud_ai

from app.db import db

from app.handlers.cliente_handler import router as clientes_router
from app.handlers.comercio_handler import router as comercios_router
from app.handlers.cuenta_handler import router as cuenta_router
from app.handlers.dispositivo_handler import router as dispositivo_router
from app.handlers.ubicacion_handler import router as ubicacion_router
from app.handlers.transaccion_handler import router as transacciones_router
from app.handlers.relaciones_handler import router as relaciones_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    db.connect()
    print("Iniciando entrenamiento de IA...", flush=True)
    fraud_ai.train_from_csv()
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


app.include_router(clientes_router)
app.include_router(comercios_router)
app.include_router(cuenta_router)
app.include_router(dispositivo_router)
app.include_router(ubicacion_router)
app.include_router(transacciones_router)
app.include_router(relaciones_router)



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
    
@app.get("/test-ia")
def test_ia():
    return {
        "entrenado": fraud_ai.is_trained,
        "modelo_path_existe": os.path.exists("fraud_model.pkl")
    }