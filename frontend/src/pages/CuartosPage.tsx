import { useEffect, useState } from "react";
import api from "../lib/api";
const errMsg=(e:any)=> e?.response?.data?.detail ? JSON.stringify(e.response.data.detail) : "Error";
export default function CuartosPage() {
  const [items,setItems]=useState<any[]>([]); const [error,setError]=useState("");
  const [form,setForm]=useState<any>({id_casa: '', numero_cuarto: '', descripcion: '', precio_alquiler: '', estado: 'libre', observacion: ''});
  const load=async()=>{try{setError(""); const {data}=await api.get('/api/cuartos'); setItems(data);}catch(e:any){setError(errMsg(e));}};
  useEffect(()=>{load();},[]);
  const create=async(e:React.FormEvent)=>{e.preventDefault(); try{
      const payload:any={...form};
      if (payload.id_casa === "") payload.id_casa=null; else payload.id_casa=Number(payload.id_casa);
      if (payload.precio_alquiler === "") payload.precio_alquiler=null; else payload.precio_alquiler=Number(payload.precio_alquiler);
      Object.keys(payload).forEach((k)=>{ if(payload[k]==="") payload[k]=null; });
      await api.post('/api/cuartos',payload); setForm({id_casa: '', numero_cuarto: '', descripcion: '', precio_alquiler: '', estado: 'libre', observacion: ''}); await load();
    }catch(e:any){setError(errMsg(e));}};
  return <div><h2>Cuartos</h2><button onClick={load}>Recargar</button>{error&&<p style={{color:'red'}}>{error}</p>}<form onSubmit={create} style={{display:'grid',gap:8,maxWidth:420,margin:'12px 0'}}><input placeholder="id_casa" value={form.id_casa} onChange={(e)=>setForm({...form,id_casa:e.target.value})} /><input placeholder="numero_cuarto" value={form.numero_cuarto} onChange={(e)=>setForm({...form,numero_cuarto:e.target.value})} /><input placeholder="descripcion" value={form.descripcion} onChange={(e)=>setForm({...form,descripcion:e.target.value})} /><input placeholder="precio_alquiler" value={form.precio_alquiler} onChange={(e)=>setForm({...form,precio_alquiler:e.target.value})} /><input placeholder="estado" value={form.estado} onChange={(e)=>setForm({...form,estado:e.target.value})} /><input placeholder="observacion" value={form.observacion} onChange={(e)=>setForm({...form,observacion:e.target.value})} /><button type='submit'>Crear</button></form><table border={1} cellPadding={6}><thead><tr>{items[0] && Object.keys(items[0]).slice(0,8).map((k)=> <th key={k}>{k}</th>)}</tr></thead><tbody>{items.map((r,i)=><tr key={i}>{Object.keys(r).slice(0,8).map((k)=><td key={k}>{String(r[k])}</td>)}</tr>)}</tbody></table></div>;
}
