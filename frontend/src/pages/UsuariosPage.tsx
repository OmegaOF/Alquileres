import { useEffect, useState } from "react";
import api from "../lib/api";
import { Card, DataTable, ErrorMessage, FormInput, PageHeader, errorMessage } from "../components/ui";

const initialForm = {nombre: '', correo: '', telefono: '', password: '', rol: 'admin', estado: 'activo'};
const fields = Object.keys(initialForm);

export default function UsuariosPage() {
  const [items,setItems]=useState<any[]>([]); const [error,setError]=useState("");
  const [form,setForm]=useState<any>(initialForm);
  const load=async()=>{try{setError(""); const {data}=await api.get('/api/usuarios'); setItems(data);}catch(e:any){setError(errorMessage(e));}};
  useEffect(()=>{load();},[]);
  const create=async(e:React.FormEvent)=>{e.preventDefault(); try{
      const payload:any={...form};
      Object.keys(payload).forEach((k)=>{ if(payload[k]==="") payload[k]=null; });
      await api.post('/api/usuarios',payload); setForm(initialForm); await load();
    }catch(e:any){setError(errorMessage(e));}};
  return <div className="page"><PageHeader title="Usuarios" description="Gestiona las personas con acceso al sistema y su información básica." action={<button className="btn btn-secondary" onClick={load}>Recargar</button>} /><ErrorMessage message={error}/><Card title="Nuevo usuario" description="Completa los mismos campos actuales para crear un acceso."><form onSubmit={create}><div className="form-grid">{fields.map(k=><FormInput key={k} label={k} value={form[k]} type={k === 'password' ? 'password' : 'text'} onChange={(v)=>setForm({...form,[k]:v})}/>)}</div><div className="form-actions"><button className="btn btn-primary" type="submit">Guardar usuario</button><button className="btn btn-secondary" type="button" onClick={()=>setForm(initialForm)}>Cancelar</button></div></form></Card><Card title="Listado de usuarios" description="Usuarios registrados actualmente."><DataTable rows={items} columns={["id_usuario","nombre","correo","telefono","rol","estado","fecha_creacion","fecha_actualizacion"]} getKey={(r)=>r.id_usuario}/></Card></div>;
}
