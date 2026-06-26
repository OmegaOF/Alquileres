from datetime import date, datetime
from decimal import Decimal
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field
class CobroMensualCreate(BaseModel): id_periodo:int; id_alquiler:int; id_casa:int; id_cuarto:int; id_inquilino:int; monto_alquiler:Decimal=Field(ge=0); monto_servicios:Decimal=Field(default=0,ge=0); deuda_anterior:Decimal=Field(default=0,ge=0); descuentos:Decimal=Field(default=0,ge=0); recargos:Decimal=Field(default=0,ge=0); fecha_limite_pago:date|None=None; observacion:str|None=None; estado_recordatorio:str="no_preparado"; fecha_ultimo_contacto:datetime|None=None; observacion_recordatorio:str|None=None
class CobroMensualUpdate(BaseModel): monto_alquiler:Decimal|None=Field(default=None,ge=0); monto_servicios:Decimal|None=Field(default=None,ge=0); deuda_anterior:Decimal|None=Field(default=None,ge=0); descuentos:Decimal|None=Field(default=None,ge=0); recargos:Decimal|None=Field(default=None,ge=0); fecha_limite_pago:date|None=None; estado:Literal["pendiente","parcial","pagado","atrasado","anulado"]|None=None; observacion:str|None=None; estado_recordatorio:str|None=None; observacion_recordatorio:str|None=None
class CobroMensualResponse(BaseModel): model_config=ConfigDict(from_attributes=True); id_cobro:int; id_periodo:int; id_alquiler:int; id_casa:int; id_cuarto:int; id_inquilino:int; monto_alquiler:Decimal; monto_servicios:Decimal; deuda_anterior:Decimal; descuentos:Decimal; recargos:Decimal; total_a_pagar:Decimal; total_pagado:Decimal; saldo_pendiente:Decimal; fecha_limite_pago:date|None=None; estado:str; fecha_generacion:datetime; observacion:str|None=None; estado_recordatorio:str="no_preparado"; fecha_ultimo_contacto:datetime|None=None; observacion_recordatorio:str|None=None

class DetalleCobroMensualResponse(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    id_detalle_cobro:int
    id_detalle:int
    id_cobro:int
    tipo_concepto:str
    concepto:str
    monto:Decimal
    descripcion:str|None=None
    id_servicio_mensual:int|None=None

class CobroDetalleResponse(CobroMensualResponse):
    detalles:list[DetalleCobroMensualResponse]=[]

class RecordatorioUpdate(BaseModel): estado:Literal["no_preparado","preparado","enviado_manual","pendiente_envio","respondio","dijo_pago","pendiente_confirmar_pago","confirmado","sin_respuesta","error_envio"]; observacion:str|None=None
