from pydantic import BaseModel
from datetime import date
from typing import Optional

class CuentaBase(BaseModel):
    saldo: float
    fecha_creacion: date
    estado: bool  # True para Activa, False para Inactiva/Bloqueada
    promedio_uso: float
    horario_promedio_uso: str

class CuentaCreate(CuentaBase):
    id: int

class CuentaUpdate(BaseModel):
    saldo: Optional[float] = None
    estado: Optional[bool] = None
    promedio_uso: Optional[float] = None
    horario_promedio_uso: Optional[str] = None