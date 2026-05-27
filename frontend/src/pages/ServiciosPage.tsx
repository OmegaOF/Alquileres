import { useEffect, useState } from "react";
import api from "../lib/api";
const errMsg=(e:any)=> e?.response?.data?.detail ? JSON.stringify(e.response.data.detail) : "Error";
export default function ServiciosPage() {
  const [items,setItems]=useState<any[]>([]); const [error,setError]=useState("");
  const [form,setForm]=useState<any>({nombre_servicio: '', descripcion: '', estado: 'activo'});
  const load=async()=>{try{setError(""); const {data}=await api.get('/api/servicios'); setItems(data);}catch(e:any){setError(errMsg(e));}};
  useEffect(()=>{load();},[]);
  const create=async(e:React.FormEvent)=>{e.preventDefault(); try{
      const payload:any={...form};
      
      Object.keys(payload).forEach((k)=>{ if(payload[k]==="") payload[k]=null; });
      await api.post('/api/servicios',payload); setForm({nombre_servicio: '', descripcion: '', estado: 'activo'}); await load();
    }catch(e:any){setError(errMsg(e));}};
  return <div><h2>Servicios</h2><button onClick={load}>Recargar</button>{error&&<p style={{color:'red'}}>{error}</p>}<form onSubmit={create} style={{display:'grid',gap:8,maxWidth:420,margin:'12px 0'}}><input placeholder="nombre_servicio" value={form.nombre_servicio} onChange={(e)=>setForm({...form,nombre_servicio:e.target.value})} /><input placeholder="descripcion" value={form.descripcion} onChange={(e)=>setForm({...form,descripcion:e.target.value})} /><input placeholder="estado" value={form.estado} onChange={(e)=>setForm({...form,estado:e.target.value})} /><button type='submit'>Crear</button></form><table border={1} cellPadding={6}><thead><tr>{items[0] && Object.keys(items[0]).slice(0,8).map((k)=> <th key={k}>{k}</th>)}</tr></thead><tbody>{items.map((r,i)=><tr key={i}>{Object.keys(r).slice(0,8).map((k)=><td key={k}>{String(r[k])}</td>)}</tr>)}</tbody></table></div>;
}
