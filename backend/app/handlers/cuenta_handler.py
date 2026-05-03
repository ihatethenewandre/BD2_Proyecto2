from fastapi import APIRouter, HTTPException
from app.db import db
from app.schemas.cuenta_schema import CuentaCreate, CuentaUpdate

router = APIRouter(prefix="/cuentas", tags=["Cuentas"])

class CuentasHandler:
    @staticmethod
    def create(cuenta: CuentaCreate):
        query = """
        CREATE (c:Cuenta {
            id: $id, 
            saldo: $saldo, 
            fecha_creacion: date($fecha_creacion), 
            estado: $estado, 
            promedio_uso: $promedio_uso, 
            horario_promedio_uso: $horario_promedio_uso
        })
        RETURN c
        """
        params = cuenta.model_dump()
        params['fecha_creacion'] = str(params['fecha_creacion'])
        result = db.run_write(query, params)
        return result["records"][0] if result["records"] else None

    @staticmethod
    def get_all(limit: int = 100):
        query = "MATCH (c:Cuenta) RETURN c LIMIT $limit"
        return db.run_query(query, {"limit": limit})

    @staticmethod
    def get_by_id(cuenta_id: int):
        query = "MATCH (c:Cuenta {id: $id}) RETURN c"
        result = db.run_query(query, {"id": cuenta_id})
        return result[0] if result else None

    @staticmethod
    def update(cuenta_id: int, cuenta: CuentaUpdate):
        update_data = {k: v for k, v in cuenta.model_dump().items() if v is not None}
        if not update_data:
            raise HTTPException(status_code=400, detail="No hay campos para actualizar")
            
        query = "MATCH (c:Cuenta {id: $id}) SET c += $props RETURN c"
        result = db.run_write(query, {"id": cuenta_id, "props": update_data})
        return result["records"][0] if result["records"] else None

    @staticmethod
    def delete(cuenta_id: int):
        query = "MATCH (c:Cuenta {id: $id}) DETACH DELETE c"
        return db.run_write(query, {"id": cuenta_id})




# --- ENDPOINTS ---

@router.post("/")
def crear_cuenta(cuenta: CuentaCreate):
    return CuentasHandler.create(cuenta)

@router.get("/")
def listar_cuentas(limit: int = 100):
    return CuentasHandler.get_all(limit)

@router.get("/{cuenta_id}")
def obtener_cuenta(cuenta_id: int):
    res = CuentasHandler.get_by_id(cuenta_id)
    if not res:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    return res

@router.put("/{cuenta_id}")
def actualizar_cuenta(cuenta_id: int, cuenta: CuentaUpdate):
    res = CuentasHandler.update(cuenta_id, cuenta)
    if not res:
        raise HTTPException(status_code=404, detail="Cuenta no encontrada")
    return res

@router.delete("/{cuenta_id}")
def eliminar_cuenta(cuenta_id: int):
    return CuentasHandler.delete(cuenta_id)