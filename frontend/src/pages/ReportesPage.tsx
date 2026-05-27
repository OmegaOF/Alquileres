import { useState } from "react";
import api from "../lib/api";
export default function ReportesPage(){
  const [idPeriodo,setIdPeriodo]=useState(""); const [idCasa,setIdCasa]=useState(""); const [resumen,setResumen]=useState<any>(null); const [casa,setCasa]=useState<any>(null); const [error,setError]=useState("");
  const cargarResumen=async()=>{try{setError(""); const {data}=await api.get(`/api/reportes/resumen-periodo/${idPeriodo}`); setResumen(data);}catch(e:any){setError(e?.response?.data?.detail||'Error');}};
  const cargarCasa=async()=>{try{setError(""); const {data}=await api.get(`/api/reportes/casa/${idCasa}/periodo/${idPeriodo}`); setCasa(data);}catch(e:any){setError(e?.response?.data?.detail||'Error');}};
  return <div><h2>Reportes</h2>{error&&<p style={{color:'red'}}>{error}</p>}<div style={{display:'flex',gap:8}}><input placeholder='id_periodo' value={idPeriodo} onChange={(e)=>setIdPeriodo(e.target.value)} /><button onClick={cargarResumen}>Resumen periodo</button></div><div style={{display:'flex',gap:8,marginTop:8}}><input placeholder='id_casa' value={idCasa} onChange={(e)=>setIdCasa(e.target.value)} /><button onClick={cargarCasa}>Reporte casa</button></div>{resumen && <pre>{JSON.stringify(resumen,null,2)}</pre>}{casa && <pre>{JSON.stringify(casa,null,2)}</pre>}</div>;
}
