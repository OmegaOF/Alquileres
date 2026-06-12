import { useEffect, useState } from "react";
import api from "../lib/api";
import { Card, DataTable, ErrorMessage, Field, PageHeader, errorMessage, formatMoney } from "../components/ui";

export default function CobrosPage(){
  const [items,setItems]=useState<any[]>([]); const [error,setError]=useState(""); const [idPeriodo,setIdPeriodo]=useState("");
  const load=async()=>{try{setError(""); const {data}=await api.get('/api/cobros');setItems(data);}catch(e:any){setError(errorMessage(e));}};
  useEffect(()=>{load();},[]);
  const generar=async()=>{try{setError(""); await api.post(`/api/cobros/generar-periodo/${idPeriodo}`); await load();}catch(e:any){setError(e?.response?.data?.detail||'Error generar');}};
  const buscarPeriodo=async()=>{try{setError(""); const {data}=await api.get(`/api/periodos/${idPeriodo}/cobros`); setItems(data);}catch{try{const {data}=await api.get(`/api/cobros/periodo/${idPeriodo}`); setItems(data);}catch(e:any){setError(e?.response?.data?.detail||'Error consulta');}}};
  const total = items.reduce((acc, x)=>acc + Number(x.total_a_pagar || 0), 0);
  const pagado = items.reduce((acc, x)=>acc + Number(x.total_pagado || 0), 0);
  const pendiente = items.reduce((acc, x)=>acc + Number(x.saldo_pendiente || 0), 0);
  return <div className="page"><PageHeader title="Cobros" description="Genera y revisa los cobros mensuales por periodo." action={<button className="btn btn-secondary" onClick={load}>Recargar</button>} /><ErrorMessage message={error}/><div className="stats-grid"><div className="stat-card blue"><span className="stat-label">Cobros visibles</span><strong className="stat-value">{items.length}</strong></div><div className="stat-card green"><span className="stat-label">Total pagado</span><strong className="stat-value">{formatMoney(pagado)}</strong></div><div className="stat-card purple"><span className="stat-label">Total a cobrar</span><strong className="stat-value">{formatMoney(total)}</strong></div><div className="stat-card orange"><span className="stat-label">Saldo pendiente</span><strong className="stat-value">{formatMoney(pendiente)}</strong></div></div><Card title="Generación por periodo" description="Mantén el mismo flujo actual: ingresa el ID de periodo para generar o consultar cobros."><div className="form-grid"><Field label="ID periodo"><input value={idPeriodo} placeholder="Ej. 1" onChange={(e)=>setIdPeriodo(e.target.value)} /></Field></div><div className="form-actions"><button className="btn btn-primary" onClick={generar}>Generar cobros</button><button className="btn btn-secondary" onClick={buscarPeriodo}>Ver por periodo</button></div></Card><Card title="Listado de cobros" description="Estado financiero de cada cobro generado."><DataTable rows={items} columns={["id_cobro","id_periodo","id_inquilino","id_cuarto","monto_alquiler","monto_servicios","deuda_anterior","total_a_pagar","total_pagado","saldo_pendiente","estado"]} getKey={(r)=>r.id_cobro}/></Card></div>;
}
