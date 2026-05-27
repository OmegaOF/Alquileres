import { useEffect, useState } from "react";
import api from "../lib/api";
const errMsg=(e:any)=> e?.response?.data?.detail ? JSON.stringify(e.response.data.detail) : "Error";
export default function ServiciosMensualesPage() {
  const [items,setItems]=useState<any[]>([]); const [error,setError]=useState("");
  const [form,setForm]=useState<any>({id_periodo: '', id_servicio: '', id_casa: '', id_cuarto: '', monto: '', responsable_pago: 'inquilino', estado_pago: 'pendiente', metodo_pago: '', fecha_pago: '', numero_comprobante: '', observacion: ''});
  const load=async()=>{try{setError(""); const {data}=await api.get('/api/servicios-mensuales'); setItems(data);}catch(e:any){setError(errMsg(e));}};
  useEffect(()=>{load();},[]);
  const create=async(e:React.FormEvent)=>{e.preventDefault(); try{
      const payload:any={...form};
      if (payload.id_periodo === "") payload.id_periodo=null; else payload.id_periodo=Number(payload.id_periodo);
      if (payload.id_servicio === "") payload.id_servicio=null; else payload.id_servicio=Number(payload.id_servicio);
      if (payload.id_casa === "") payload.id_casa=null; else payload.id_casa=Number(payload.id_casa);
      if (payload.id_cuarto === "") payload.id_cuarto=null; else payload.id_cuarto=Number(payload.id_cuarto);
      if (payload.monto === "") payload.monto=null; else payload.monto=Number(payload.monto);
      Object.keys(payload).forEach((k)=>{ if(payload[k]==="") payload[k]=null; });
      await api.post('/api/servicios-mensuales',payload); setForm({id_periodo: '', id_servicio: '', id_casa: '', id_cuarto: '', monto: '', responsable_pago: 'inquilino', estado_pago: 'pendiente', metodo_pago: '', fecha_pago: '', numero_comprobante: '', observacion: ''}); await load();
    }catch(e:any){setError(errMsg(e));}};
  return <div><h2>ServiciosMensuales</h2><button onClick={load}>Recargar</button>{error&&<p style={{color:'red'}}>{error}</p>}<form onSubmit={create} style={{display:'grid',gap:8,maxWidth:420,margin:'12px 0'}}><input placeholder="id_periodo" value={form.id_periodo} onChange={(e)=>setForm({...form,id_periodo:e.target.value})} /><input placeholder="id_servicio" value={form.id_servicio} onChange={(e)=>setForm({...form,id_servicio:e.target.value})} /><input placeholder="id_casa" value={form.id_casa} onChange={(e)=>setForm({...form,id_casa:e.target.value})} /><input placeholder="id_cuarto" value={form.id_cuarto} onChange={(e)=>setForm({...form,id_cuarto:e.target.value})} /><input placeholder="monto" value={form.monto} onChange={(e)=>setForm({...form,monto:e.target.value})} /><input placeholder="responsable_pago" value={form.responsable_pago} onChange={(e)=>setForm({...form,responsable_pago:e.target.value})} /><input placeholder="estado_pago" value={form.estado_pago} onChange={(e)=>setForm({...form,estado_pago:e.target.value})} /><input placeholder="metodo_pago" value={form.metodo_pago} onChange={(e)=>setForm({...form,metodo_pago:e.target.value})} /><input placeholder="fecha_pago" value={form.fecha_pago} onChange={(e)=>setForm({...form,fecha_pago:e.target.value})} /><input placeholder="numero_comprobante" value={form.numero_comprobante} onChange={(e)=>setForm({...form,numero_comprobante:e.target.value})} /><input placeholder="observacion" value={form.observacion} onChange={(e)=>setForm({...form,observacion:e.target.value})} /><button type='submit'>Crear</button></form><table border={1} cellPadding={6}><thead><tr>{items[0] && Object.keys(items[0]).slice(0,8).map((k)=> <th key={k}>{k}</th>)}</tr></thead><tbody>{items.map((r,i)=><tr key={i}>{Object.keys(r).slice(0,8).map((k)=><td key={k}>{String(r[k])}</td>)}</tr>)}</tbody></table></div>;
}
