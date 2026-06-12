import { useEffect, useState } from "react";
import api from "../lib/api";
import { Card, DataTable, ErrorMessage, FormInput, PageHeader, errorMessage } from "../components/ui";
const initialForm = {nombre_servicio: '', descripcion: '', estado: 'activo'};
const fields = Object.keys(initialForm);
export default function ServiciosPage() {
  const [items,setItems]=useState<any[]>([]); const [error,setError]=useState(""); const [form,setForm]=useState<any>(initialForm);
  const load=async()=>{try{setError(""); const {data}=await api.get('/api/servicios'); setItems(data);}catch(e:any){setError(errorMessage(e));}}; useEffect(()=>{load();},[]);
  const create=async(e:React.FormEvent)=>{e.preventDefault(); try{ const payload:any={...form}; Object.keys(payload).forEach((k)=>{ if(payload[k]==="") payload[k]=null; }); await api.post('/api/servicios',payload); setForm(initialForm); await load(); }catch(e:any){setError(errorMessage(e));}};
  return <div className="page"><PageHeader title="Servicios" description="Mantén el catálogo de servicios usados en cobros y egresos." action={<button className="btn btn-secondary" onClick={load}>Recargar</button>} /><ErrorMessage message={error}/><Card title="Nuevo servicio" description="Agrega un concepto reutilizable para periodos mensuales."><form onSubmit={create}><div className="form-grid">{fields.map(k=><FormInput key={k} label={k} value={form[k]} onChange={(v)=>setForm({...form,[k]:v})}/>)}</div><div className="form-actions"><button className="btn btn-primary" type="submit">Guardar servicio</button><button className="btn btn-secondary" type="button" onClick={()=>setForm(initialForm)}>Cancelar</button></div></form></Card><Card title="Listado de servicios" description="Catálogo disponible."><DataTable rows={items} columns={["id_servicio","nombre_servicio","descripcion","estado"]} getKey={(r)=>r.id_servicio}/></Card></div>;
}
