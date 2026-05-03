from fastapi import APIRouter, HTTPException
from app.db import db
from app.schemas.comercio_schema import ComercioCreate, ComercioUpdate

router = APIRouter(prefix="/comercios", tags=["Comercios"])

class ComerciosHandler:
    @staticmethod
    def create(comercio: ComercioCreate):
        query = """
        CREATE (c:Comercio {
            id: $id, 
            nombre: $nombre, 
            categoria: $categoria, 
            tipo: $tipo, 
            horario_operacion: $horario_operacion, 
            riesgo: $riesgo
        })
        RETURN c
        """
        params = comercio.model_dump()
        result = db.run_write(query, params)
        return result["records"][0] if result["records"] else None

    @staticmethod
    def get_all(limit: int = 100):
        query = "MATCH (c:Comercio) RETURN c LIMIT $limit"
        return db.run_query(query, {"limit": limit})

    @staticmethod
    def get_by_id(comercio_id: int):
        query = "MATCH (c:Comercio {id: $id}) RETURN c"
        result = db.run_query(query, {"id": comercio_id})
        return result[0] if result else None

    @staticmethod
    def update(comercio_id: int, comercio: ComercioUpdate):
        update_data = {k: v for k, v in comercio.model_dump().items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="No hay campos para actualizar")
            
        query = "MATCH (c:Comercio {id: $id}) SET c += $props RETURN c"
        result = db.run_write(query, {"id": comercio_id, "props": update_data})
        return result["records"][0] if result["records"] else None

    @staticmethod
    def delete(comercio_id: int):
        query = "MATCH (c:Comercio {id: $id}) DETACH DELETE c"
        return db.run_write(query, {"id": comercio_id})

    @staticmethod
    def bulk_add_prop(categoria: str, prop: str, valor: str):
        """Punto: Agregar/Actualizar propiedad a múltiples nodos"""
        query = f"MATCH (c:Comercio {{categoria: $cat}}) SET c.{prop} = $val RETURN count(c) as total"
        return db.run_write(query, {"cat": categoria, "val": valor})

    @staticmethod
    def bulk_remove_prop(categoria: str, prop: str):
        """Punto: Eliminar propiedad de múltiples nodos"""
        query = f"MATCH (c:Comercio {{categoria: $cat}}) REMOVE c.{prop} RETURN count(c) as total"
        return db.run_write(query, {"cat": categoria})
    


# --- ENDPOINTS ---

@router.post("/")
def crear_comercio(comercio: ComercioCreate):
    return ComerciosHandler.create(comercio)

@router.get("/")
def listar_comercios(limit: int = 100):
    return ComerciosHandler.get_all(limit)

@router.get("/{comercio_id}")
def obtener_comercio(comercio_id: int):
    res = ComerciosHandler.get_by_id(comercio_id)
    if not res:
        raise HTTPException(status_code=404, detail="Comercio no encontrado")
    return res

@router.put("/{comercio_id}")
def actualizar_comercio(comercio_id: int, comercio: ComercioUpdate):
    res = ComerciosHandler.update(comercio_id, comercio)
    if not res:
        raise HTTPException(status_code=404, detail="Comercio no encontrado")
    return res

@router.delete("/{comercio_id}")
def eliminar_comercio(comercio_id: int):
    return ComerciosHandler.delete(comercio_id)

@router.put("/masivo/propiedad")
def agregar_prop_masivo(categoria: str, propiedad: str, valor: str):
    return ComerciosHandler.bulk_add_prop(categoria, propiedad, valor)

@router.delete("/masivo/propiedad")
def eliminar_prop_masiva(categoria: str, propiedad: str):
    return ComerciosHandler.bulk_remove_prop(categoria, propiedad)
