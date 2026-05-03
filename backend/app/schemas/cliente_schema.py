from pydantic import BaseModel
from datetime import date
from typing import Optional

class ClienteBase(BaseModel):
    nombre: str
    fecha_nacimiento: date
    riesgo: float
    sueldo: float
    empleo: str

class ClienteCreate(ClienteBase):
    id: int

class ClienteUpdate(BaseModel):
    nombre: Optional[str] = None
    riesgo: Optional[float] = None
    sueldo: Optional[float] = None
    empleo: Optional[str] = None

class ClienteResponse(ClienteBase):
    id: int