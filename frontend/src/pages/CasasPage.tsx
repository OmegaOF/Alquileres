import { useEffect, useState } from "react";
import api from "../lib/api";
import { Card, DataTable, ErrorMessage, FormInput, PageHeader, errorMessage } from "../components/ui";
const initialForm = {nombre_casa: '', direccion: '', zona: '', ciudad: '', descripcion: '', estado: 'activa', id_usuario_responsable: ''};
const fields = Object.keys(initialForm);
export default function CasasPage() {
  const [items,setItems]=useState<any[]>([]); const [error,setError]=useState("");
  const [form,setForm]=useState<any>(initialForm);
  const load=async()=>{try{setError(""); const {data}=await api.get('/api/casas'); setItems(data);}catch(e:any){setError(errorMessage(e));}};
  useEffect(()=>{load();},[]);
  const create=async(e:React.FormEvent)=>{e.preventDefault(); try{ const payload:any={...form}; if (payload.id_usuario_responsable === "") payload.id_usuario_responsable=null; else payload.id_usuario_responsable=Number(payload.id_usuario_responsable); Object.keys(payload).forEach((k)=>{ if(payload[k]==="") payload[k]=null; }); await api.post('/api/casas',payload); setForm(initialForm); await load(); }catch(e:any){setError(errorMessage(e));}};
  return <div className="page"><PageHeader title="Casas" description="Administra propiedades, direcciones y responsables." action={<button className="btn btn-secondary" onClick={load}>Recargar</button>} /><ErrorMessage message={error}/><Card title="Nueva casa" description="Registra una propiedad con su responsable."><form onSubmit={create}><div className="form-grid">{fields.map(k=><FormInput key={k} label={k} value={form[k]} onChange={(v)=>setForm({...form,[k]:v})}/>)}</div><div className="form-actions"><button className="btn btn-primary" type="submit">Guardar casa</button><button className="btn btn-secondary" type="button" onClick={()=>setForm(initialForm)}>Cancelar</button></div></form></Card><Card title="Listado de casas" description="Propiedades registradas."><DataTable rows={items} columns={["id_casa","nombre_casa","direccion","zona","ciudad","estado","id_usuario_responsable","fecha_creacion"]} getKey={(r)=>r.id_casa}/></Card></div>;
}
