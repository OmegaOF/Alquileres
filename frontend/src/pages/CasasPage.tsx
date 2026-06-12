import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import api from "../lib/api";
import { Card, DataTable, ErrorMessage, FormInput, PageHeader, errorMessage } from "../components/ui";

const initialForm = {nombre_casa: '', direccion: '', zona: '', ciudad: '', descripcion: '', estado: 'activa', id_usuario_responsable: ''};
const fields = Object.keys(initialForm);

function CasaDetalle({ idCasa }: { idCasa: string }) {
  const [casa,setCasa]=useState<any>(null); const [cuartos,setCuartos]=useState<any[]>([]); const [error,setError]=useState("");
  const load=async()=>{try{setError(""); const [{data:casaData},{data:cuartosData}]=await Promise.all([api.get(`/api/casas/${idCasa}`), api.get(`/api/casas/${idCasa}/cuartos`)]); setCasa(casaData); setCuartos(cuartosData);}catch(e:any){setError(errorMessage(e));}};
  useEffect(()=>{load();},[idCasa]);
  return <div className="page"><PageHeader title={casa?.nombre_casa || `Casa ${idCasa}`} description="Detalle de propiedad y acceso contextual a sus cuartos." action={<Link className="btn btn-secondary" to="/casas">Volver a casas</Link>} /><ErrorMessage message={error}/><Card title="Detalle de casa" description="Información registrada de la propiedad."><div className="detail-grid"><div><strong>Dirección</strong><span>{casa?.direccion || '—'}</span></div><div><strong>Zona</strong><span>{casa?.zona || '—'}</span></div><div><strong>Ciudad</strong><span>{casa?.ciudad || '—'}</span></div><div><strong>Estado</strong><span>{casa?.estado || '—'}</span></div></div></Card><Card title="Cuartos de esta casa" description="Administra únicamente los cuartos relacionados a esta propiedad." action={<Link className="btn btn-primary" to={`/casas/${idCasa}/cuartos/nuevo`}>Crear cuarto</Link>}><DataTable rows={cuartos} columns={["id_cuarto","numero_cuarto","descripcion","precio_alquiler","estado","observacion"]} getKey={(r)=>r.id_cuarto} actions={(r)=><Link className="btn btn-secondary btn-sm" to={`/cuartos/${r.id_cuarto}`}>Ver cuarto</Link>}/></Card></div>;
}

export default function CasasPage() {
  const { idCasa } = useParams();
  const [items,setItems]=useState<any[]>([]); const [error,setError]=useState("");
  const [form,setForm]=useState<any>(initialForm);
  const load=async()=>{try{setError(""); const {data}=await api.get('/api/casas'); setItems(data);}catch(e:any){setError(errorMessage(e));}};
  useEffect(()=>{if(!idCasa) load();},[idCasa]);
  if (idCasa) return <CasaDetalle idCasa={idCasa} />;
  const create=async(e:React.FormEvent)=>{e.preventDefault(); try{ const payload:any={...form}; if (payload.id_usuario_responsable === "") payload.id_usuario_responsable=null; else payload.id_usuario_responsable=Number(payload.id_usuario_responsable); Object.keys(payload).forEach((k)=>{ if(payload[k]==="") payload[k]=null; }); await api.post('/api/casas',payload); setForm(initialForm); await load(); }catch(e:any){setError(errorMessage(e));}};
  return <div className="page"><PageHeader title="Casas" description="Área de propiedades: administra casas y desde cada una crea sus cuartos." action={<button className="btn btn-secondary" onClick={load}>Recargar</button>} /><ErrorMessage message={error}/><Card title="Nueva casa" description="Registra una propiedad con su responsable."><form onSubmit={create}><div className="form-grid">{fields.map(k=><FormInput key={k} label={k} value={form[k]} onChange={(v)=>setForm({...form,[k]:v})}/>)}</div><div className="form-actions"><button className="btn btn-primary" type="submit">Guardar casa</button><button className="btn btn-secondary" type="button" onClick={()=>setForm(initialForm)}>Cancelar</button></div></form></Card><Card title="Listado de casas" description="Usa las acciones para ver detalle o administrar cuartos en contexto."><DataTable rows={items} columns={["id_casa","nombre_casa","direccion","zona","ciudad","estado","id_usuario_responsable","fecha_creacion"]} getKey={(r)=>r.id_casa} actions={(r)=><div className="action-row"><Link className="btn btn-secondary btn-sm" to={`/casas/${r.id_casa}`}>Ver detalle</Link><Link className="btn btn-primary btn-sm" to={`/casas/${r.id_casa}/cuartos`}>Administrar cuartos</Link></div>}/></Card></div>;
}
