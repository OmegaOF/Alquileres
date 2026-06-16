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

class CasaResumenResponse(BaseModel):
    id_casa:int
    nombre_casa:str
    direccion:str
    zona:str|None=None
    ciudad:str|None=None
    estado:str
    total_cuartos:int
    cuartos_libres:int
    cuartos_ocupados:int

class CuartoCasaResumenResponse(BaseModel):
    id_cuarto:int
    id_casa:int
    numero_cuarto:str
    descripcion:str|None=None
    estado:str
    precio_alquiler:float
    id_alquiler_activo:int|None=None
    monto_alquiler_activo:float|None=None
    id_inquilino_actual:int|None=None
    nombre_inquilino_actual:str|None=None
    telefono_inquilino_actual:str|None=None
    fecha_inicio_alquiler_activo:str|None=None
    saldo_pendiente_alquiler_activo:float|None=None
