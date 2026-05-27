from typing import Literal
from pydantic import BaseModel, ConfigDict
class ServicioCreate(BaseModel): nombre_servicio:str; descripcion:str|None=None; estado:Literal["activo","inactivo"]="activo"
class ServicioUpdate(BaseModel): nombre_servicio:str|None=None; descripcion:str|None=None; estado:Literal["activo","inactivo"]|None=None
class ServicioResponse(BaseModel): model_config=ConfigDict(from_attributes=True); id_servicio:int; nombre_servicio:str; descripcion:str|None=None; estado:str
