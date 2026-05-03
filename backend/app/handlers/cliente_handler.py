from fastapi import APIRouter, HTTPException
from app.db import db
from app.schemas.cliente_schema import ClienteCreate, ClienteUpdate
from typing import List

router = APIRouter(prefix="/clientes", tags=["Clientes"])

class ClientesHandler:
    @staticmethod
    def create(cliente: ClienteCreate):
        query = """
        CREATE (c:Cliente {
            id: $id, 
            nombre: $nombre, 
            fecha_nacimiento: date($fecha_nacimiento), 
            riesgo: $riesgo, 
            sueldo: $sueldo, 
            empleo: $empleo
        })
        RETURN c
        """
        params = cliente.model_dump()
        params['fecha_nacimiento'] = str(params['fecha_nacimiento'])
        result = db.run_write(query, params)
        return result["records"][0] if result["records"] else None

    @staticmethod
    def get_all(limit: int = 100):
        query = "MATCH (c:Cliente) RETURN c LIMIT $limit"
        return db.run_query(query, {"limit": limit})

    @staticmethod
    def get_by_id(cliente_id: int):
        query = "MATCH (c:Cliente {id: $id}) RETURN c"
        result = db.run_query(query, {"id": cliente_id})
        return result[0] if result else None

    @staticmethod
    def update(cliente_id: int, cliente: ClienteUpdate):
        update_data = {k: v for k, v in cliente.model_dump().items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="No hay campos para actualizar")
            
        query = "MATCH (c:Cliente {id: $id}) SET c += $props RETURN c"
        result = db.run_write(query, {"id": cliente_id, "props": update_data})
        return result["records"][0] if result["records"] else None

    @staticmethod
    def delete(cliente_id: int):
        query = "MATCH (c:Cliente {id: $id}) DETACH DELETE c"
        return db.run_write(query, {"id": cliente_id})




# --- ENDPOINTS (Rutas de FastAPI) ---

@router.post("/")
def crear_cliente(cliente: ClienteCreate):
    return ClientesHandler.create(cliente)

@router.get("/")
def listar_clientes(limit: int = 100):
    return ClientesHandler.get_all(limit)

@router.get("/{cliente_id}")
def obtener_cliente(cliente_id: int):
    cliente = ClientesHandler.get_by_id(cliente_id)
    if not cliente:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return cliente

@router.put("/{cliente_id}")
def actualizar_cliente(cliente_id: int, cliente: ClienteUpdate):
    res = ClientesHandler.update(cliente_id, cliente)
    if not res:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    return res

@router.delete("/{cliente_id}")
def eliminar_cliente(cliente_id: int):
    return ClientesHandler.delete(cliente_id)