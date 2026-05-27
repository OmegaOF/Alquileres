from datetime import datetime
from decimal import Decimal
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field
class PagoCreate(BaseModel): id_cobro:int; id_detalle_cobro:int|None=None; id_inquilino:int; monto_pagado:Decimal=Field(gt=0); fecha_pago:datetime|None=None; metodo_pago:str|None=None; numero_comprobante:str|None=None; imagen_comprobante:str|None=None; registrado_por:int; observacion:str|None=None; estado:Literal["valido","anulado"]="valido"
class PagoUpdate(BaseModel): id_detalle_cobro:int|None=None; monto_pagado:Decimal|None=Field(default=None,gt=0); fecha_pago:datetime|None=None; metodo_pago:str|None=None; numero_comprobante:str|None=None; imagen_comprobante:str|None=None; registrado_por:int|None=None; observacion:str|None=None; estado:Literal["valido","anulado"]|None=None
class PagoResponse(BaseModel): model_config=ConfigDict(from_attributes=True); id_pago:int; id_cobro:int; id_detalle_cobro:int|None=None; id_inquilino:int; monto_pagado:Decimal; fecha_pago:datetime; metodo_pago:str|None=None; numero_comprobante:str|None=None; imagen_comprobante:str|None=None; registrado_por:int; observacion:str|None=None; estado:str
