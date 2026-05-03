from pydantic import BaseModel
from typing import Optional

class ComercioBase(BaseModel):
    nombre: str
    categoria: str
    tipo: str  # online / fisico
    horario_operacion: str
    riesgo: bool

class ComercioCreate(ComercioBase):
    id: int

class ComercioUpdate(BaseModel):
    nombre: Optional[str] = None
    categoria: Optional[str] = None
    tipo: Optional[str] = None
    horario_operacion: Optional[str] = None
    riesgo: Optional[bool] = None