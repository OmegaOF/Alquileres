import { useEffect, useState } from "react";
import api from "../lib/api";
const errMsg=(e:any)=> e?.response?.data?.detail ? JSON.stringify(e.response.data.detail) : "Error";
export default function PagosPage(){
  const [items,setItems]=useState<any[]>([]); const [error,setError]=useState("");
  const [form,setForm]=useState<any>({id_cobro:"",id_detalle_cobro:"",id_inquilino:"",monto_pagado:"",metodo_pago:"",numero_comprobante:"",imagen_comprobante:"",registrado_por:"",observacion:"",estado:"valido"});
  const load=async()=>{try{setError("");const {data}=await api.get('/api/pagos');setItems(data);}catch(e:any){setError(errMsg(e));}};
  useEffect(()=>{load();},[]);
  const create=async(e:React.FormEvent)=>{e.preventDefault(); try{const payload:any={...form}; ['id_cobro','id_detalle_cobro','id_inquilino','registrado_por','monto_pagado'].forEach((k)=> payload[k]=payload[k]===""?null:Number(payload[k])); Object.keys(payload).forEach(k=>payload[k]===""&&(payload[k]=null)); await api.post('/api/pagos',payload); await load();}catch(e:any){setError(errMsg(e));}};
  const anular=async(id:number)=>{try{await api.post(`/api/pagos/${id}/anular`); await load();}catch(e:any){setError(errMsg(e));}};
  return <div><h2>Pagos</h2><button onClick={load}>Recargar</button>{error&&<p style={{color:'red'}}>{error}</p>}<form onSubmit={create} style={{display:'grid',gap:8,maxWidth:420}}>{Object.keys(form).map(k=><input key={k} placeholder={k} value={form[k]} onChange={(e)=>setForm({...form,[k]:e.target.value})} />)}<button>Crear</button></form><table border={1}><thead><tr><th>id</th><th>cobro</th><th>monto</th><th>estado</th><th>acción</th></tr></thead><tbody>{items.map((x)=><tr key={x.id_pago}><td>{x.id_pago}</td><td>{x.id_cobro}</td><td>{x.monto_pagado}</td><td>{x.estado}</td><td><button onClick={()=>anular(x.id_pago)}>Anular</button></td></tr>)}</tbody></table></div>;
}
