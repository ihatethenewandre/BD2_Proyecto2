from fastapi import APIRouter, HTTPException
from app.db import db
from app.schemas.cliente_schema import ClienteCreate, ClienteUpdate
from typing import List
from datetime import datetime

router = APIRouter(prefix="/clientes", tags=["Clientes"])

class ClientesHandler:
    @staticmethod
    def create(cliente: ClienteCreate):
        query = """
        CREATE (c:Cliente {
            id: $id, 
            nombre: $nombre, 
            fecha_nacimiento: datetime($fecha_nacimiento), 
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



    #requisitos adicionales de rúbrica 
    @staticmethod
    def promote_to_premium_suspect(cliente_id: int):
        """
        Punto: Creación de nodos con 2+ labels (via SET/MERGE)
        Añade labels adicionales a un nodo existente.
        """
        query = """
        MATCH (c:Cliente {id: $id})
        SET c:Sospechoso:Alarmante
        RETURN labels(c) as etiquetas, c.nombre as nombre
        """
        return db.run_write(query, {"id": cliente_id})

    @staticmethod
    def get_stats():
        """
        Punto: Realizar consultas agregadas de datos
        """
        query = """
        MATCH (c:Cliente)
        RETURN 
            count(c) as total_clientes, 
            avg(c.sueldo) as sueldo_promedio, 
            max(c.riesgo) as riesgo_maximo
        """
        return db.run_query(query)

    @staticmethod
    def remove_node_property(cliente_id: int, prop_name: str):
        """Punto: Eliminar propiedad de un nodo"""
        query = f"MATCH (c:Cliente {{id: $id}}) REMOVE c.{prop_name} RETURN c"
        result = db.run_write(query, {"id": cliente_id})
        return result["records"][0] if result["records"] else None




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

##adicionales, de rubrica


@router.put("/nivelAlerta/{cliente_id}")
def colocar_alerta(cliente_id:int):
    return ClientesHandler.promote_to_premium_suspect(cliente_id=cliente_id)

@router.get("/stats/resumen")
def estadisticas_clientes():
    return ClientesHandler.get_stats()

@router.delete("/{cliente_id}/propiedad/{prop_name}")
def eliminar_prop_nodo(cliente_id: int, prop_name: str): 
    return ClientesHandler.remove_node_property(cliente_id, prop_name)