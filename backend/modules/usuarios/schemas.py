from datetime import datetime
from pydantic import BaseModel, ConfigDict
class UsuarioCreate(BaseModel): nombre:str; correo:str; telefono:str|None=None; password:str; rol:str="admin"; estado:str="activo"
class UsuarioUpdate(BaseModel): nombre:str|None=None; correo:str|None=None; telefono:str|None=None; password:str|None=None; rol:str|None=None; estado:str|None=None
class UsuarioResponse(BaseModel): model_config=ConfigDict(from_attributes=True); id_usuario:int; nombre:str; correo:str; telefono:str|None=None; rol:str; estado:str; fecha_creacion:datetime; fecha_actualizacion:datetime
