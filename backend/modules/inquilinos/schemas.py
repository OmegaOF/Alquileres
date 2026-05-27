from datetime import datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict

class InquilinoCreate(BaseModel):
    nombre:str
    ci:str|None=None
    telefono:str|None=None
    correo:str|None=None
    direccion_referencia:str|None=None
    contacto_emergencia:str|None=None
    telefono_emergencia:str|None=None
    estado:Literal["activo","inactivo"]="activo"
    observacion:str|None=None

class InquilinoUpdate(BaseModel):
    nombre:str|None=None
    ci:str|None=None
    telefono:str|None=None
    correo:str|None=None
    direccion_referencia:str|None=None
    contacto_emergencia:str|None=None
    telefono_emergencia:str|None=None
    estado:Literal["activo","inactivo"]|None=None
    observacion:str|None=None

class InquilinoResponse(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id_inquilino:int
    nombre:str
    ci:str|None=None
    telefono:str|None=None
    correo:str|None=None
    direccion_referencia:str|None=None
    contacto_emergencia:str|None=None
    telefono_emergencia:str|None=None
    estado:str
    observacion:str|None=None
    fecha_creacion:datetime
    fecha_actualizacion:datetime
