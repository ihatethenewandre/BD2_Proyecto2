from pydantic import BaseModel
from datetime import date, time
from typing import Optional

class TransaccionBase(BaseModel):
    monto: float
    fecha: date
    hora: time
    es_fraudulenta: bool

class TransaccionCreate(TransaccionBase):
    id: int

class TransaccionUpdate(BaseModel):
    monto: Optional[float] = None
    es_fraudulenta: Optional[bool] = None