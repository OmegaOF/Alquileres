from datetime import datetime
from decimal import Decimal
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

class CuartoCreate(BaseModel):
    id_casa:int
    numero_cuarto:str
    descripcion:str|None=None
    precio_alquiler:Decimal=Field(ge=0)
    estado:Literal["libre","ocupado","reservado","mantenimiento"]="libre"
    observacion:str|None=None

class CuartoUpdate(BaseModel):
    id_casa:int|None=None
    numero_cuarto:str|None=None
    descripcion:str|None=None
    precio_alquiler:Decimal|None=Field(default=None, ge=0)
    estado:Literal["libre","ocupado","reservado","mantenimiento"]|None=None
    observacion:str|None=None

class CuartoResponse(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id_cuarto:int
    id_casa:int
    numero_cuarto:str
    descripcion:str|None=None
    precio_alquiler:Decimal
    estado:str
    observacion:str|None=None
    fecha_creacion:datetime
    fecha_actualizacion:datetime
