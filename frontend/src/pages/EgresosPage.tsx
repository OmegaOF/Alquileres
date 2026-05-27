import { useEffect, useState } from "react";
import api from "../lib/api";
const errMsg=(e:any)=> e?.response?.data?.detail ? JSON.stringify(e.response.data.detail) : "Error";
export default function EgresosPage() {
  const [items,setItems]=useState<any[]>([]); const [error,setError]=useState("");
  const [form,setForm]=useState<any>({id_casa: '', id_periodo: '', id_cuarto: '', id_servicio_mensual: '', concepto: '', categoria: 'otro', monto: '', fecha_egreso: '', metodo_pago: '', numero_comprobante: '', comprobante: '', observacion: '', registrado_por: ''});
  const load=async()=>{try{setError(""); const {data}=await api.get('/api/egresos'); setItems(data);}catch(e:any){setError(errMsg(e));}};
  useEffect(()=>{load();},[]);
  const create=async(e:React.FormEvent)=>{e.preventDefault(); try{
      const payload:any={...form};
      if (payload.id_casa === "") payload.id_casa=null; else payload.id_casa=Number(payload.id_casa);
      if (payload.id_periodo === "") payload.id_periodo=null; else payload.id_periodo=Number(payload.id_periodo);
      if (payload.id_cuarto === "") payload.id_cuarto=null; else payload.id_cuarto=Number(payload.id_cuarto);
      if (payload.id_servicio_mensual === "") payload.id_servicio_mensual=null; else payload.id_servicio_mensual=Number(payload.id_servicio_mensual);
      if (payload.monto === "") payload.monto=null; else payload.monto=Number(payload.monto);
      if (payload.registrado_por === "") payload.registrado_por=null; else payload.registrado_por=Number(payload.registrado_por);
      Object.keys(payload).forEach((k)=>{ if(payload[k]==="") payload[k]=null; });
      await api.post('/api/egresos',payload); setForm({id_casa: '', id_periodo: '', id_cuarto: '', id_servicio_mensual: '', concepto: '', categoria: 'otro', monto: '', fecha_egreso: '', metodo_pago: '', numero_comprobante: '', comprobante: '', observacion: '', registrado_por: ''}); await load();
    }catch(e:any){setError(errMsg(e));}};
  return <div><h2>Egresos</h2><button onClick={load}>Recargar</button>{error&&<p style={{color:'red'}}>{error}</p>}<form onSubmit={create} style={{display:'grid',gap:8,maxWidth:420,margin:'12px 0'}}><input placeholder="id_casa" value={form.id_casa} onChange={(e)=>setForm({...form,id_casa:e.target.value})} /><input placeholder="id_periodo" value={form.id_periodo} onChange={(e)=>setForm({...form,id_periodo:e.target.value})} /><input placeholder="id_cuarto" value={form.id_cuarto} onChange={(e)=>setForm({...form,id_cuarto:e.target.value})} /><input placeholder="id_servicio_mensual" value={form.id_servicio_mensual} onChange={(e)=>setForm({...form,id_servicio_mensual:e.target.value})} /><input placeholder="concepto" value={form.concepto} onChange={(e)=>setForm({...form,concepto:e.target.value})} /><input placeholder="categoria" value={form.categoria} onChange={(e)=>setForm({...form,categoria:e.target.value})} /><input placeholder="monto" value={form.monto} onChange={(e)=>setForm({...form,monto:e.target.value})} /><input placeholder="fecha_egreso" value={form.fecha_egreso} onChange={(e)=>setForm({...form,fecha_egreso:e.target.value})} /><input placeholder="metodo_pago" value={form.metodo_pago} onChange={(e)=>setForm({...form,metodo_pago:e.target.value})} /><input placeholder="numero_comprobante" value={form.numero_comprobante} onChange={(e)=>setForm({...form,numero_comprobante:e.target.value})} /><input placeholder="comprobante" value={form.comprobante} onChange={(e)=>setForm({...form,comprobante:e.target.value})} /><input placeholder="observacion" value={form.observacion} onChange={(e)=>setForm({...form,observacion:e.target.value})} /><input placeholder="registrado_por" value={form.registrado_por} onChange={(e)=>setForm({...form,registrado_por:e.target.value})} /><button type='submit'>Crear</button></form><table border={1} cellPadding={6}><thead><tr>{items[0] && Object.keys(items[0]).slice(0,8).map((k)=> <th key={k}>{k}</th>)}</tr></thead><tbody>{items.map((r,i)=><tr key={i}>{Object.keys(r).slice(0,8).map((k)=><td key={k}>{String(r[k])}</td>)}</tr>)}</tbody></table></div>;
}
