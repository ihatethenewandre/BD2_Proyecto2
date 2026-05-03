from fastapi import APIRouter, HTTPException
from app.db import db
from app.schemas.ubicacion_schema import UbicacionCreate, UbicacionUpdate

router = APIRouter(prefix="/ubicaciones", tags=["Ubicaciones"])

class UbicacionesHandler:
    @staticmethod
    def create(ubicacion: UbicacionCreate):
        query = """
        CREATE (u:Ubicacion {
            id: $id, 
            continente: $continente, 
            pais: $pais, 
            ciudad: $ciudad, 
            latitud: $latitud, 
            longitud: $longitud, 
            zona_riesgo: $zona_riesgo
        })
        RETURN u
        """
        params = ubicacion.model_dump()
        result = db.run_write(query, params)
        return result["records"][0] if result["records"] else None

    @staticmethod
    def get_all(limit: int = 100):
        query = "MATCH (u:Ubicacion) RETURN u LIMIT $limit"
        return db.run_query(query, {"limit": limit})

    @staticmethod
    def get_by_id(ubicacion_id: int):
        query = "MATCH (u:Ubicacion {id: $id}) RETURN u"
        result = db.run_query(query, {"id": ubicacion_id})
        return result[0] if result else None

    @staticmethod
    def update(ubicacion_id: int, ubicacion: UbicacionUpdate):
        update_data = {k: v for k, v in ubicacion.model_dump().items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="No hay campos para actualizar")
            
        query = "MATCH (u:Ubicacion {id: $id}) SET u += $props RETURN u"
        result = db.run_write(query, {"id": ubicacion_id, "props": update_data})
        return result["records"][0] if result["records"] else None

    @staticmethod
    def delete(ubicacion_id: int):
        query = "MATCH (u:Ubicacion {id: $id}) DETACH DELETE u"
        return db.run_write(query, {"id": ubicacion_id})





# --- ENDPOINTS ---

@router.post("/")
def crear_ubicacion(ubicacion: UbicacionCreate):
    return UbicacionesHandler.create(ubicacion)

@router.get("/")
def listar_ubicaciones(limit: int = 100):
    return UbicacionesHandler.get_all(limit)

@router.get("/{ubicacion_id}")
def obtener_ubicacion(ubicacion_id: int):
    res = UbicacionesHandler.get_by_id(ubicacion_id)
    if not res:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    return res

@router.put("/{ubicacion_id}")
def actualizar_ubicacion(ubicacion_id: int, ubicacion: UbicacionUpdate):
    res = UbicacionesHandler.update(ubicacion_id, ubicacion)
    if not res:
        raise HTTPException(status_code=404, detail="Ubicación no encontrada")
    return res

@router.delete("/{ubicacion_id}")
def eliminar_ubicacion(ubicacion_id: int):
    return UbicacionesHandler.delete(ubicacion_id)