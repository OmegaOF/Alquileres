import { useEffect, useState } from "react";
import api from "../lib/api";
const errMsg=(e:any)=> e?.response?.data?.detail ? JSON.stringify(e.response.data.detail) : "Error";
export default function PeriodosPage() {
  const [items,setItems]=useState<any[]>([]); const [error,setError]=useState("");
  const [form,setForm]=useState<any>({anio: '', mes: '', nombre_periodo: '', fecha_inicio: '', fecha_fin: '', estado: 'abierto'});
  const load=async()=>{try{setError(""); const {data}=await api.get('/api/periodos'); setItems(data);}catch(e:any){setError(errMsg(e));}};
  useEffect(()=>{load();},[]);
  const create=async(e:React.FormEvent)=>{e.preventDefault(); try{
      const payload:any={...form};
      if (payload.anio === "") payload.anio=null; else payload.anio=Number(payload.anio);
      if (payload.mes === "") payload.mes=null; else payload.mes=Number(payload.mes);
      Object.keys(payload).forEach((k)=>{ if(payload[k]==="") payload[k]=null; });
      await api.post('/api/periodos',payload); setForm({anio: '', mes: '', nombre_periodo: '', fecha_inicio: '', fecha_fin: '', estado: 'abierto'}); await load();
    }catch(e:any){setError(errMsg(e));}};
  return <div><h2>Periodos</h2><button onClick={load}>Recargar</button>{error&&<p style={{color:'red'}}>{error}</p>}<form onSubmit={create} style={{display:'grid',gap:8,maxWidth:420,margin:'12px 0'}}><input placeholder="anio" value={form.anio} onChange={(e)=>setForm({...form,anio:e.target.value})} /><input placeholder="mes" value={form.mes} onChange={(e)=>setForm({...form,mes:e.target.value})} /><input placeholder="nombre_periodo" value={form.nombre_periodo} onChange={(e)=>setForm({...form,nombre_periodo:e.target.value})} /><input placeholder="fecha_inicio" value={form.fecha_inicio} onChange={(e)=>setForm({...form,fecha_inicio:e.target.value})} /><input placeholder="fecha_fin" value={form.fecha_fin} onChange={(e)=>setForm({...form,fecha_fin:e.target.value})} /><input placeholder="estado" value={form.estado} onChange={(e)=>setForm({...form,estado:e.target.value})} /><button type='submit'>Crear</button></form><table border={1} cellPadding={6}><thead><tr>{items[0] && Object.keys(items[0]).slice(0,8).map((k)=> <th key={k}>{k}</th>)}</tr></thead><tbody>{items.map((r,i)=><tr key={i}>{Object.keys(r).slice(0,8).map((k)=><td key={k}>{String(r[k])}</td>)}</tr>)}</tbody></table></div>;
}
