from pydantic import BaseModel, Field
from typing import List
from datetime import datetime

class OfertaBase(BaseModel):
    producto_ids: List[int] = Field(..., min_items=1)
    descuentos: List[float] = Field(..., min_items=1)
    fecha_vencimiento: datetime

class OfertaCreate(OfertaBase):
    pass

class OfertaUpdate(BaseModel):
    producto_ids: List[int] = None
    descuentos: List[float] = None
    fecha_vencimiento: datetime = None

class OfertaResponse(OfertaBase):
    id: int
    fecha_creacion: datetime
    fecha_actualizacion: datetime

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            producto_ids=obj.producto_ids,
            descuentos=obj.descuentos,
            fecha_vencimiento=obj.fecha_vencimiento,
            fecha_creacion=obj.fecha_creacion,
            fecha_actualizacion=obj.fecha_actualizacion
        )

    class Config:
        from_attributes = True