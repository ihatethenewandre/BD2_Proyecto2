from pydantic import BaseModel
from typing import Optional

class UbicacionBase(BaseModel):
    continente: str
    pais: str
    ciudad: str
    latitud: float
    longitud: float
    zona_riesgo: bool

class UbicacionCreate(UbicacionBase):
    id: int

class UbicacionUpdate(BaseModel):
    continente: Optional[str] = None
    pais: Optional[str] = None
    ciudad: Optional[str] = None
    latitud: Optional[float] = None
    longitud: Optional[float] = None
    zona_riesgo: Optional[bool] = None