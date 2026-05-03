from fastapi import APIRouter, HTTPException
from app.db import db
from app.schemas.transaccion_schema import TransaccionCreate, TransaccionUpdate

router = APIRouter(prefix="/transacciones", tags=["Transacciones"])

class TransaccionesHandler:
    @staticmethod
    def create(transaccion: TransaccionCreate):
        query = """
        CREATE (t:Transaccion {
            id: $id, 
            monto: $monto, 
            fecha: date($fecha), 
            hora: time($hora), 
            es_fraudulenta: $es_fraudulenta
        })
        RETURN t
        """
        params = transaccion.model_dump()
        params['fecha'] = str(params['fecha'])
        params['hora'] = str(params['hora'])
        
        result = db.run_write(query, params)
        return result["records"][0] if result["records"] else None

    @staticmethod
    def get_all(limit: int = 100):
        query = "MATCH (t:Transaccion) RETURN t LIMIT $limit"
        return db.run_query(query, {"limit": limit})

    @staticmethod
    def get_by_id(transaccion_id: int):
        query = "MATCH (t:Transaccion {id: $id}) RETURN t"
        result = db.run_query(query, {"id": transaccion_id})
        return result[0] if result else None

    @staticmethod
    def update(transaccion_id: int, transaccion: TransaccionUpdate):
        update_data = {k: v for k, v in transaccion.model_dump().items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="No hay campos para actualizar")
            
        query = "MATCH (t:Transaccion {id: $id}) SET t += $props RETURN t"
        result = db.run_write(query, {"id": transaccion_id, "props": update_data})
        return result["records"][0] if result["records"] else None

    @staticmethod
    def delete(transaccion_id: int):
        query = "MATCH (t:Transaccion {id: $id}) DETACH DELETE t"
        return db.run_write(query, {"id": transaccion_id})




# --- ENDPOINTS ---

@router.post("/")
def crear_transaccion(transaccion: TransaccionCreate):
    return TransaccionesHandler.create(transaccion)

@router.get("/")
def listar_transacciones(limit: int = 100):
    return TransaccionesHandler.get_all(limit)

@router.get("/{transaccion_id}")
def obtener_transaccion(transaccion_id: int):
    res = TransaccionesHandler.get_by_id(transaccion_id)
    if not res:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return res

@router.put("/{transaccion_id}")
def actualizar_transaccion(transaccion_id: int, transaccion: TransaccionUpdate):
    res = TransaccionesHandler.update(transaccion_id, transaccion)
    if not res:
        raise HTTPException(status_code=404, detail="Transacción no encontrada")
    return res

@router.delete("/{transaccion_id}")
def eliminar_transaccion(transaccion_id: int):
    return TransaccionesHandler.delete(transaccion_id)