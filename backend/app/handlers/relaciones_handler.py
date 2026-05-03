from fastapi import APIRouter, HTTPException
from app.db import db
from pydantic import BaseModel
from typing import Dict, Any, Optional
from datetime import datetime

router = APIRouter(prefix="/relaciones", tags=["Relaciones"])

class RelacionRequest(BaseModel):
    id_origen: int
    id_destino: int
    propiedades: Dict[str, Any]

class RelacionesHandler:
    
    @staticmethod
    def crear_relacion_especifica(tipo: str, origen_label: str, destino_label: str, data: RelacionRequest):
        """
        Crea cualquiera de tus 10 relaciones usando los nombres exactos.
        """
        query = f"""
        MATCH (a:{origen_label} {{id: $id_a}})
        MATCH (b:{destino_label} {{id: $id_b}})
        CREATE (a)-[r:{tipo} $props]->(b)
        RETURN r
        """
        return db.run_write(query, {
            "id_a": data.id_origen, 
            "id_b": data.id_destino, 
            "props": data.propiedades
        })

    @staticmethod
    def registrar_flujo_fraude(data: dict):
        """
        Versión final ajustada a ZONED DATETIME y nombres de tu BD.
        """
        query = """
        MATCH (cu:Cuenta {id: $cuenta_id})
        MATCH (co:Comercio {id: $comercio_id})
        MATCH (di:Dispositivo {id: $dispositivo_id})
        
        CREATE (t:Transaccion {
            id: $t_id, 
            monto: $monto, 
            fecha: datetime($fecha_trans), 
            hora: $hora, 
            es_fraudulenta: $es_fraudulenta
        })
        
        # Usamos los nombres y props exactas de tu tabla de relaciones
        CREATE (cu)-[:REALIZA {
            fecha: datetime($fecha_trans), 
            canal: $canal, 
            autenticado: $autenticado
        }]->(t)
        
        CREATE (t)-[:REALIZADA_EN {
            fecha: datetime($fecha_trans), 
            metodo_pago: $metodo, 
            presencial: $presencial
        }]->(co)
        
        CREATE (t)-[:USANDO {
            fecha: datetime($fecha_trans), 
            ip: $ip, 
            autenticacion_fuerte: $auth_fuerte
        }]->(di)
        
        RETURN t
        """
        return db.run_write(query, data)

    # --- MÉTODOS DE RÚBRICA (MASIVOS) ---
    @staticmethod
    def bulk_update_rel(tipo_rel: str, prop: str, valor: Any):
        query = f"MATCH ()-[r:{tipo_rel}]->() SET r.{prop} = $val RETURN count(r) as total"
        return db.run_write(query, {"val": valor})

    @staticmethod
    def bulk_remove_rel_prop(tipo_rel: str, prop: str):
        query = f"MATCH ()-[r:{tipo_rel}]->() REMOVE r.{prop} RETURN count(r) as total"
        return db.run_write(query)

# --- ENDPOINTS ---

@router.post("/vincular/{tipo_relacion}")
def vincular_nodos(tipo_relacion: str, data: RelacionRequest):
    """
    Usa este endpoint para cualquiera de las 10 relaciones.
    Ejemplo de tipo_relacion: POSEE, DESTINO, UBICADO_EN, USA, RESIDE_EN...
    """
    # Mapeo simple de etiquetas para seguridad
    mapeo = {
        "POSEE": ("Cliente", "Cuenta"),
        "REALIZA": ("Cuenta", "Transaccion"),
        "DESTINO": ("Transaccion", "Cuenta"),
        "REALIZADA_EN": ("Transaccion", "Comercio"),
        "USANDO": ("Transaccion", "Dispositivo"),
        "UBICADO_EN": ("Dispositivo", "Ubicacion"), # También aplica a Comercio-Ubicacion
        "USA": ("Cliente", "Dispositivo"),
        "RESIDE_EN": ("Cliente", "Ubicacion"),
        "ASOCIADA_A_DISPOSITIVO": ("Cuenta", "Dispositivo")
    }
    
    if tipo_relacion not in mapeo and tipo_relacion != "UBICADO_EN_COMERCIO":
        raise HTTPException(400, "Tipo de relación no configurada")
    
    # Caso especial para UBICADO_EN que se repite en Dispositivo y Comercio
    if tipo_relacion == "UBICADO_EN":
        # Por defecto asumimos Dispositivo. Si se quiere Comercio, usar un flag 
        labels = ("Dispositivo", "Ubicacion")
    else:
        labels = mapeo[tipo_relacion]

    return RelacionesHandler.crear_relacion_especifica(tipo_relacion, labels[0], labels[1], data)

@router.post("/flujo-transaccion-completa")
def flujo_completo(
    t_id: int, cuenta_id: int, comercio_id: int, dispositivo_id: int,
    monto: float, canal: str, metodo: str, presencial: bool, ip: str
):
    #Frontend debe enviar fecha en formato ISO (2026-05-02T21:30:00Z)
    payload = {
        "t_id": t_id, "cuenta_id": cuenta_id, "comercio_id": comercio_id,
        "dispositivo_id": dispositivo_id, "monto": monto, 
        "fecha_trans": datetime.now().isoformat(), # Ajuste a Zoned DateTime
        "hora": datetime.now().strftime("%H:%M:%S"),
        "es_fraudulenta": False,
        "canal": canal, "autenticado": True, "metodo": metodo, 
        "presencial": presencial, "ip": ip, "auth_fuerte": True
    }
    return RelacionesHandler.registrar_flujo_fraude(payload)


@router.put("/masivo/propiedad")
def actualizar_prop_relacion(tipo: str, propiedad: str, valor: str):
    return RelacionesHandler.bulk_update_rel(tipo, propiedad, valor)

@router.delete("/masivo/propiedad")
def eliminar_prop_relacion(tipo: str, propiedad: str):
    return RelacionesHandler.bulk_remove_rel_prop(tipo, propiedad)
