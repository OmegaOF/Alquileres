from datetime import date, datetime
from decimal import Decimal
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

class AlquilerCreate(BaseModel):
    id_inquilino:int
    id_cuarto:int
    fecha_inicio:date
    fecha_fin:date|None=None
    monto_alquiler:Decimal=Field(ge=0)
    modalidad_alquiler:Literal["mensual","diario"]="mensual"
    monto_mensual:Decimal|None=Field(default=None, ge=0)
    precio_diario:Decimal|None=Field(default=None, ge=0)
    total_alquiler_diario:Decimal|None=Field(default=None, ge=0)
    dia_pago:int=Field(ge=1,le=31)
    garantia:Decimal|None=Field(default=None, ge=0)
    estado:Literal["activo","finalizado","cancelado"]="activo"
    observacion:str|None=None

class AlquilerUpdate(BaseModel):
    id_inquilino:int|None=None
    id_cuarto:int|None=None
    fecha_inicio:date|None=None
    fecha_fin:date|None=None
    monto_alquiler:Decimal|None=Field(default=None, ge=0)
    modalidad_alquiler:Literal["mensual","diario"]|None=None
    monto_mensual:Decimal|None=Field(default=None, ge=0)
    precio_diario:Decimal|None=Field(default=None, ge=0)
    total_alquiler_diario:Decimal|None=Field(default=None, ge=0)
    dia_pago:int|None=Field(default=None, ge=1, le=31)
    garantia:Decimal|None=Field(default=None, ge=0)
    estado:Literal["activo","finalizado","cancelado"]|None=None
    observacion:str|None=None

class AlquilerResponse(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id_alquiler:int
    id_inquilino:int
    id_cuarto:int
    fecha_inicio:date
    fecha_fin:date|None=None
    monto_alquiler:Decimal
    modalidad_alquiler:str="mensual"
    monto_mensual:Decimal|None=None
    precio_diario:Decimal|None=None
    total_alquiler_diario:Decimal|None=None
    dia_pago:int
    garantia:Decimal|None=None
    estado:str
    observacion:str|None=None
    fecha_creacion:datetime
    fecha_actualizacion:datetime
