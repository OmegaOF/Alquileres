from pydantic import BaseModel
class PeriodoResumen(BaseModel):
    id_periodo:int; anio:int; mes:int; estado:str
class PropiedadesResumen(BaseModel):
    total_casas:int; total_cuartos:int; cuartos_libres:int; cuartos_ocupados:int; alquileres_activos:int
class FinanzasResumen(BaseModel):
    total_facturado:float; total_pagado:float; saldo_pendiente:float; total_egresos:float; resultado_actual:float
class CobrosResumen(BaseModel):
    pendientes:int; parciales:int; pagados:int; atrasados:int
class DashboardResumen(BaseModel):
    periodo:PeriodoResumen|None; propiedades:PropiedadesResumen; finanzas:FinanzasResumen; cobros:CobrosResumen
