from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict

class CasaCreate(BaseModel):
    nombre_casa:str
    direccion:str
    zona:str|None=None
    ciudad:str|None=None
    descripcion:str|None=None
    estado:Literal["activa","inactiva","mantenimiento"]="activa"
    id_usuario_responsable:int

class CasaUpdate(BaseModel):
    nombre_casa:str|None=None
    direccion:str|None=None
    zona:str|None=None
    ciudad:str|None=None
    descripcion:str|None=None
    estado:Literal["activa","inactiva","mantenimiento"]|None=None
    id_usuario_responsable:int|None=None

class CasaResponse(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id_casa:int
    nombre_casa:str
    direccion:str
    zona:str|None=None
    ciudad:str|None=None
    descripcion:str|None=None
    estado:str
    id_usuario_responsable:int
    fecha_creacion:datetime
    fecha_actualizacion:datetime
