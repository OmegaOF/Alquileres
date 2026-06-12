import { useEffect, useState } from "react";
import api from "../lib/api";
import { Card, DataTable, ErrorMessage, FormInput, PageHeader, errorMessage } from "../components/ui";
const initialForm = {anio: '', mes: '', nombre_periodo: '', fecha_inicio: '', fecha_fin: '', estado: 'abierto'};
const fields = Object.keys(initialForm);
export default function PeriodosPage() {
  const [items,setItems]=useState<any[]>([]); const [error,setError]=useState(""); const [form,setForm]=useState<any>(initialForm);
  const load=async()=>{try{setError(""); const {data}=await api.get('/api/periodos'); setItems(data);}catch(e:any){setError(errorMessage(e));}}; useEffect(()=>{load();},[]);
  const create=async(e:React.FormEvent)=>{e.preventDefault(); try{ const payload:any={...form}; if (payload.anio === "") payload.anio=null; else payload.anio=Number(payload.anio); if (payload.mes === "") payload.mes=null; else payload.mes=Number(payload.mes); Object.keys(payload).forEach((k)=>{ if(payload[k]==="") payload[k]=null; }); await api.post('/api/periodos',payload); setForm(initialForm); await load(); }catch(e:any){setError(errorMessage(e));}};
  return <div className="page"><PageHeader title="Periodos" description="Define meses de operación para generar cobros y reportes." action={<button className="btn btn-secondary" onClick={load}>Recargar</button>} /><ErrorMessage message={error}/><Card title="Nuevo periodo" description="Registra año, mes y rango de fechas del periodo."><form onSubmit={create}><div className="form-grid">{fields.map(k=><FormInput key={k} label={k} value={form[k]} onChange={(v)=>setForm({...form,[k]:v})}/>)}</div><div className="form-actions"><button className="btn btn-primary" type="submit">Guardar periodo</button><button className="btn btn-secondary" type="button" onClick={()=>setForm(initialForm)}>Cancelar</button></div></form></Card><Card title="Listado de periodos" description="Periodos mensuales creados."><DataTable rows={items} columns={["id_periodo","anio","mes","nombre_periodo","fecha_inicio","fecha_fin","estado","fecha_creacion"]} getKey={(r)=>r.id_periodo}/></Card></div>;
}
