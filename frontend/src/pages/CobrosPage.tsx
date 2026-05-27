import { useEffect, useState } from "react";
import api from "../lib/api";
export default function CobrosPage(){
  const [items,setItems]=useState<any[]>([]); const [error,setError]=useState(""); const [idPeriodo,setIdPeriodo]=useState("");
  const load=async()=>{try{const {data}=await api.get('/api/cobros');setItems(data);}catch(e:any){setError(e?.response?.data?.detail||'Error');}};
  useEffect(()=>{load();},[]);
  const generar=async()=>{try{setError(""); await api.post(`/api/cobros/generar-periodo/${idPeriodo}`); await load();}catch(e:any){setError(e?.response?.data?.detail||'Error generar');}};
  const buscarPeriodo=async()=>{try{const {data}=await api.get(`/api/periodos/${idPeriodo}/cobros`); setItems(data);}catch{try{const {data}=await api.get(`/api/cobros/periodo/${idPeriodo}`); setItems(data);}catch(e:any){setError(e?.response?.data?.detail||'Error consulta');}}};
  return <div><h2>Cobros</h2><button onClick={load}>Recargar</button><div style={{margin:'8px 0'}}><input placeholder='id_periodo' value={idPeriodo} onChange={(e)=>setIdPeriodo(e.target.value)} /><button onClick={generar}>Generar cobros</button><button onClick={buscarPeriodo}>Ver por periodo</button></div>{error&&<p style={{color:'red'}}>{error}</p>}<table border={1}><thead><tr><th>id_cobro</th><th>id_periodo</th><th>id_inquilino</th><th>id_cuarto</th><th>monto_alquiler</th><th>monto_servicios</th><th>deuda_anterior</th><th>total_a_pagar</th><th>total_pagado</th><th>saldo_pendiente</th><th>estado</th></tr></thead><tbody>{items.map((x)=><tr key={x.id_cobro}><td>{x.id_cobro}</td><td>{x.id_periodo}</td><td>{x.id_inquilino}</td><td>{x.id_cuarto}</td><td>{x.monto_alquiler}</td><td>{x.monto_servicios}</td><td>{x.deuda_anterior}</td><td>{x.total_a_pagar}</td><td>{x.total_pagado}</td><td>{x.saldo_pendiente}</td><td>{x.estado}</td></tr>)}</tbody></table></div>;
}
