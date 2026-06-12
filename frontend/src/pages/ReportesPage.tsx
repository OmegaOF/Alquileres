import { useState } from "react";
import api from "../lib/api";
import { Card, ErrorMessage, Field, PageHeader, formatMoney } from "../components/ui";

function ReportMetric({ label, value, money = true }: { label: string; value: any; money?: boolean }) {
  return <div className="report-metric"><span>{label}</span><strong>{money ? formatMoney(value) : (value ?? "—")}</strong></div>;
}

function ReportCards({ data }: { data: any }) {
  if (!data) return <div className="empty-state">Consulta un reporte para visualizar los resultados.</div>;
  const ganancia = data.total_pagado !== undefined && data.total_egresos !== undefined ? Number(data.total_pagado) - Number(data.total_egresos) : undefined;
  return (
    <div className="report-grid">
      <ReportMetric label="Total a cobrar" value={data.total_a_cobrar} />
      <ReportMetric label="Total pagado" value={data.total_pagado} />
      <ReportMetric label="Saldo pendiente" value={data.total_pendiente} />
      <ReportMetric label="Egresos" value={data.total_egresos} />
      {ganancia !== undefined && <ReportMetric label="Ganancia estimada" value={ganancia} />}
      {data.cantidad_cobros !== undefined && <ReportMetric label="Cobros" value={data.cantidad_cobros} money={false} />}
      {data.cantidad_pagados !== undefined && <ReportMetric label="Pagados" value={data.cantidad_pagados} money={false} />}
      {data.cantidad_pendientes !== undefined && <ReportMetric label="Pendientes" value={data.cantidad_pendientes} money={false} />}
      {data.cantidad_parciales !== undefined && <ReportMetric label="Parciales" value={data.cantidad_parciales} money={false} />}
      {data.cantidad_atrasados !== undefined && <ReportMetric label="Atrasados" value={data.cantidad_atrasados} money={false} />}
      {data.cobros !== undefined && <ReportMetric label="Cobros" value={data.cobros} money={false} />}
      {data.egresos !== undefined && <ReportMetric label="Egresos registrados" value={data.egresos} money={false} />}
    </div>
  );
}

export default function ReportesPage(){
  const [idPeriodo,setIdPeriodo]=useState(""); const [idCasa,setIdCasa]=useState(""); const [resumen,setResumen]=useState<any>(null); const [casa,setCasa]=useState<any>(null); const [error,setError]=useState("");
  const cargarResumen=async()=>{try{setError(""); const {data}=await api.get(`/api/reportes/resumen-periodo/${idPeriodo}`); setResumen(data);}catch(e:any){setError(e?.response?.data?.detail||'Error');}};
  const cargarCasa=async()=>{try{setError(""); const {data}=await api.get(`/api/reportes/casa/${idCasa}/periodo/${idPeriodo}`); setCasa(data);}catch(e:any){setError(e?.response?.data?.detail||'Error');}};
  return (
    <div className="page">
      <PageHeader title="Reportes" description="Consulta totales financieros por periodo o por casa sin ver JSON crudo." />
      <ErrorMessage message={error}/>
      <Card title="Filtros de reporte" description="Ingresa los IDs requeridos y consulta la información.">
        <div className="form-grid">
          <Field label="ID periodo"><input placeholder="Ej. 1" value={idPeriodo} onChange={(e)=>setIdPeriodo(e.target.value)} /></Field>
          <Field label="ID casa"><input placeholder="Ej. 1" value={idCasa} onChange={(e)=>setIdCasa(e.target.value)} /></Field>
        </div>
        <div className="form-actions">
          <button className="btn btn-primary" onClick={cargarResumen}>Resumen periodo</button>
          <button className="btn btn-secondary" onClick={cargarCasa}>Reporte casa</button>
        </div>
      </Card>
      <Card title="Resumen del periodo" description="Totales generales del periodo seleccionado."><ReportCards data={resumen}/></Card>
      <Card title="Reporte por casa" description="Totales filtrados por casa y periodo."><ReportCards data={casa}/></Card>
    </div>
  );
}
