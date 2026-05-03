from pydantic import BaseModel
from typing import Optional

class DispositivoBase(BaseModel):
    tipo: str              # telefono, computadora, tablet
    ip: str
    sistema_operativo: str  # iOS, Android, macOS, Windows
    confiable: bool
    precio: float

class DispositivoCreate(DispositivoBase):
    id: int

class DispositivoUpdate(BaseModel):
    tipo: Optional[str] = None
    ip: Optional[str] = None
    sistema_operativo: Optional[str] = None
    confiable: Optional[bool] = None
    precio: Optional[float] = None