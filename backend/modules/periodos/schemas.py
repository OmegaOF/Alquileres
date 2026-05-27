from datetime import date, datetime
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field
class PeriodoMensualCreate(BaseModel): anio:int; mes:int=Field(ge=1,le=12); nombre_periodo:str; fecha_inicio:date; fecha_fin:date; estado:Literal["abierto","cerrado"]="abierto"
class PeriodoMensualUpdate(BaseModel): anio:int|None=None; mes:int|None=Field(default=None,ge=1,le=12); nombre_periodo:str|None=None; fecha_inicio:date|None=None; fecha_fin:date|None=None; estado:Literal["abierto","cerrado"]|None=None
class PeriodoMensualResponse(BaseModel): model_config=ConfigDict(from_attributes=True); id_periodo:int; anio:int; mes:int; nombre_periodo:str; fecha_inicio:date; fecha_fin:date; estado:str; fecha_creacion:datetime
