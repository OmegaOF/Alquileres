import { useEffect, useState } from "react";
import api from "../lib/api";

const toNum = (v: string) => (v === "" ? null : Number(v));
const errMsg = (e: any) => e?.response?.data?.detail ? JSON.stringify(e.response.data.detail) : "Error";

export default function AlquileresPage() {
  const [items, setItems] = useState<any[]>([]);
  const [error, setError] = useState("");
  const [form, setForm] = useState<any>({ id_inquilino: "", id_cuarto: "", fecha_inicio: "", fecha_fin: "", monto_alquiler: "", dia_pago: "1", garantia: "", estado: "activo", observacion: "" });

  const load = async () => { try { setError(""); const { data } = await api.get('/api/alquileres'); setItems(data); } catch (e:any) { setError(errMsg(e)); } };
  useEffect(() => { load(); }, []);

  const create = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const payload = { ...form, id_inquilino: toNum(form.id_inquilino), id_cuarto: toNum(form.id_cuarto), monto_alquiler: toNum(form.monto_alquiler), dia_pago: toNum(form.dia_pago), garantia: toNum(form.garantia), fecha_fin: form.fecha_fin || null, observacion: form.observacion || null };
      await api.post('/api/alquileres', payload); await load();
    } catch (e:any) { setError(errMsg(e)); }
  };
  const finalizar = async (id:number) => { try { await api.post(`/api/alquileres/${id}/finalizar`); await load(); } catch (e:any) { setError(errMsg(e)); } };

  return <div><h2>Alquileres</h2><button onClick={load}>Recargar</button>{error && <p style={{color:'red'}}>{error}</p>}<form onSubmit={create} style={{display:'grid',gap:8,maxWidth:420}}>{Object.keys(form).map(k => <input key={k} placeholder={k} value={form[k]} onChange={(e)=>setForm({...form,[k]:e.target.value})} />)}<button type='submit'>Crear</button></form><table border={1}><thead><tr><th>id</th><th>inquilino</th><th>cuarto</th><th>estado</th><th>acciones</th></tr></thead><tbody>{items.map(x=><tr key={x.id_alquiler}><td>{x.id_alquiler}</td><td>{x.id_inquilino}</td><td>{x.id_cuarto}</td><td>{x.estado}</td><td><button onClick={()=>finalizar(x.id_alquiler)}>Finalizar</button></td></tr>)}</tbody></table></div>;
}
