from fastapi import APIRouter, HTTPException
from app.db import db
from app.schemas.dispositivo_schema import DispositivoCreate, DispositivoUpdate

router = APIRouter(prefix="/dispositivos", tags=["Dispositivos"])

class DispositivosHandler:
    @staticmethod
    def create(dispositivo: DispositivoCreate):
        query = """
        CREATE (d:Dispositivo {
            id: $id, 
            tipo: $tipo, 
            ip: $ip, 
            sistema_operativo: $sistema_operativo, 
            confiable: $confiable, 
            precio: $precio
        })
        RETURN d
        """
        params = dispositivo.model_dump()
        result = db.run_write(query, params)
        return result["records"][0] if result["records"] else None

    @staticmethod
    def get_all(limit: int = 100):
        query = "MATCH (d:Dispositivo) RETURN d LIMIT $limit"
        return db.run_query(query, {"limit": limit})

    @staticmethod
    def get_by_id(dispositivo_id: int):
        query = "MATCH (d:Dispositivo {id: $id}) RETURN d"
        result = db.run_query(query, {"id": dispositivo_id})
        return result[0] if result else None

    @staticmethod
    def update(dispositivo_id: int, dispositivo: DispositivoUpdate):
        update_data = {k: v for k, v in dispositivo.model_dump().items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="No hay campos para actualizar")
            
        query = "MATCH (d:Dispositivo {id: $id}) SET d += $props RETURN d"
        result = db.run_write(query, {"id": dispositivo_id, "props": update_data})
        return result["records"][0] if result["records"] else None

    @staticmethod
    def delete(dispositivo_id: int):
        query = "MATCH (d:Dispositivo {id: $id}) DETACH DELETE d"
        return db.run_write(query, {"id": dispositivo_id})




# --- ENDPOINTS ---

@router.post("/")
def crear_dispositivo(dispositivo: DispositivoCreate):
    return DispositivosHandler.create(dispositivo)

@router.get("/")
def listar_dispositivos(limit: int = 100):
    return DispositivosHandler.get_all(limit)

@router.get("/{dispositivo_id}")
def obtener_dispositivo(dispositivo_id: int):
    res = DispositivosHandler.get_by_id(dispositivo_id)
    if not res:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return res

@router.put("/{dispositivo_id}")
def actualizar_dispositivo(dispositivo_id: int, dispositivo: DispositivoUpdate):
    res = DispositivosHandler.update(dispositivo_id, dispositivo)
    if not res:
        raise HTTPException(status_code=404, detail="Dispositivo no encontrado")
    return res

@router.delete("/{dispositivo_id}")
def eliminar_dispositivo(dispositivo_id: int):
    return DispositivosHandler.delete(dispositivo_id)