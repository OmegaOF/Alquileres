import { useEffect, useState } from "react";
import api from "../lib/api";
import { Card, DataTable, ErrorMessage, FormInput, PageHeader, errorMessage } from "../components/ui";
const initialForm = {nombre: '', ci: '', telefono: '', correo: '', direccion_referencia: '', contacto_emergencia: '', telefono_emergencia: '', estado: 'activo', observacion: ''};
const fields = Object.keys(initialForm);
export default function InquilinosPage() {
  const [items,setItems]=useState<any[]>([]); const [error,setError]=useState(""); const [form,setForm]=useState<any>(initialForm);
  const load=async()=>{try{setError(""); const {data}=await api.get('/api/inquilinos'); setItems(data);}catch(e:any){setError(errorMessage(e));}}; useEffect(()=>{load();},[]);
  const create=async(e:React.FormEvent)=>{e.preventDefault(); try{ const payload:any={...form}; Object.keys(payload).forEach((k)=>{ if(payload[k]==="") payload[k]=null; }); await api.post('/api/inquilinos',payload); setForm(initialForm); await load(); }catch(e:any){setError(errorMessage(e));}};
  return <div className="page"><PageHeader title="Inquilinos" description="Registra datos personales, contacto y referencias de emergencia." action={<button className="btn btn-secondary" onClick={load}>Recargar</button>} /><ErrorMessage message={error}/><Card title="Nuevo inquilino" description="Mantén actualizada la información del ocupante."><form onSubmit={create}><div className="form-grid">{fields.map(k=><FormInput key={k} label={k} value={form[k]} onChange={(v)=>setForm({...form,[k]:v})}/>)}</div><div className="form-actions"><button className="btn btn-primary" type="submit">Guardar inquilino</button><button className="btn btn-secondary" type="button" onClick={()=>setForm(initialForm)}>Cancelar</button></div></form></Card><Card title="Listado de inquilinos" description="Personas registradas para alquileres."><DataTable rows={items} columns={["id_inquilino","nombre","ci","telefono","correo","contacto_emergencia","estado","fecha_creacion"]} getKey={(r)=>r.id_inquilino}/></Card></div>;
}
