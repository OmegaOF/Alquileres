import { useEffect, useState } from "react";
import api from "../lib/api";
const errMsg=(e:any)=> e?.response?.data?.detail ? JSON.stringify(e.response.data.detail) : "Error";
export default function UsuariosPage() {
  const [items,setItems]=useState<any[]>([]); const [error,setError]=useState("");
  const [form,setForm]=useState<any>({nombre: '', correo: '', telefono: '', password: '', rol: 'admin', estado: 'activo'});
  const load=async()=>{try{setError(""); const {data}=await api.get('/api/usuarios'); setItems(data);}catch(e:any){setError(errMsg(e));}};
  useEffect(()=>{load();},[]);
  const create=async(e:React.FormEvent)=>{e.preventDefault(); try{
      const payload:any={...form};
      
      Object.keys(payload).forEach((k)=>{ if(payload[k]==="") payload[k]=null; });
      await api.post('/api/usuarios',payload); setForm({nombre: '', correo: '', telefono: '', password: '', rol: 'admin', estado: 'activo'}); await load();
    }catch(e:any){setError(errMsg(e));}};
  return <div><h2>Usuarios</h2><button onClick={load}>Recargar</button>{error&&<p style={{color:'red'}}>{error}</p>}<form onSubmit={create} style={{display:'grid',gap:8,maxWidth:420,margin:'12px 0'}}><input placeholder="nombre" value={form.nombre} onChange={(e)=>setForm({...form,nombre:e.target.value})} /><input placeholder="correo" value={form.correo} onChange={(e)=>setForm({...form,correo:e.target.value})} /><input placeholder="telefono" value={form.telefono} onChange={(e)=>setForm({...form,telefono:e.target.value})} /><input placeholder="password" value={form.password} onChange={(e)=>setForm({...form,password:e.target.value})} /><input placeholder="rol" value={form.rol} onChange={(e)=>setForm({...form,rol:e.target.value})} /><input placeholder="estado" value={form.estado} onChange={(e)=>setForm({...form,estado:e.target.value})} /><button type='submit'>Crear</button></form><table border={1} cellPadding={6}><thead><tr>{items[0] && Object.keys(items[0]).slice(0,8).map((k)=> <th key={k}>{k}</th>)}</tr></thead><tbody>{items.map((r,i)=><tr key={i}>{Object.keys(r).slice(0,8).map((k)=><td key={k}>{String(r[k])}</td>)}</tr>)}</tbody></table></div>;
}
