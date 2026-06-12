import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import api from "../lib/api";
import ContextHelp from "../components/ContextHelp";
import SearchSelect from "../components/SearchSelect";
import { BreadcrumbItem, Card, ConfirmDialog, ContextSummary, DataTable, Drawer, EmptyState, ErrorMessage, FormActions, FormInput, PageHeader, RowActionsMenu, errorMessage } from "../components/ui";

const toNum = (v: string) => (v === "" ? null : Number(v));
const initialForm = { id_inquilino: "", id_cuarto: "", fecha_inicio: "", fecha_fin: "", monto_alquiler: "", dia_pago: "1", garantia: "", estado: "activo", observacion: "" };
const contextFields = ["fecha_inicio", "fecha_fin", "monto_alquiler", "dia_pago", "garantia", "estado", "observacion"];
const requiredFields = new Set(["fecha_inicio", "monto_alquiler", "dia_pago"]);

const inquilinoLabel = (inquilino: any) => `${inquilino.nombre || `Inquilino #${inquilino.id_inquilino}`} — CI ${inquilino.ci || "sin CI"} — Tel. ${inquilino.telefono || "sin teléfono"}`;
const inquilinoSelectedLabel = (inquilino: any) => `${inquilino.nombre || `Inquilino #${inquilino.id_inquilino}`} — CI ${inquilino.ci || "sin CI"} — Tel. ${inquilino.telefono || "sin teléfono"}`;
const inquilinoSearchText = (inquilino: any) => [inquilino.id_inquilino, inquilino.nombre, inquilino.ci, inquilino.telefono, inquilino.correo].filter(Boolean).join(" ");

export default function AlquileresPage() {
  const { idCuarto } = useParams();
  const navigate = useNavigate();
  const [items, setItems] = useState<any[]>([]);
  const [inquilinos, setInquilinos] = useState<any[]>([]);
  const [error, setError] = useState("");
  const [form, setForm] = useState<any>({ ...initialForm, id_cuarto: idCuarto || "" });
  const [cuarto, setCuarto] = useState<any>(null);
  const [casa, setCasa] = useState<any>(null);
  const [confirmId, setConfirmId] = useState<number | null>(null);

  const selectedInquilino = inquilinos.find((inquilino) => String(inquilino.id_inquilino) === String(form.id_inquilino)) || null;

  const load = async () => {
    try {
      setError("");
      const [{ data: alquileresData }, { data: inquilinosData }] = await Promise.all([api.get("/api/alquileres"), api.get("/api/inquilinos")]);
      setItems(alquileresData);
      setInquilinos(inquilinosData);
      if (idCuarto) {
        const cuartoResp = await api.get(`/api/cuartos/${idCuarto}`);
        setCuarto(cuartoResp.data);
        const casaResp = await api.get(`/api/casas/${cuartoResp.data.id_casa}`);
        setCasa(casaResp.data);
        setForm((f: any) => ({ ...f, id_cuarto: idCuarto, monto_alquiler: f.monto_alquiler || String(cuartoResp.data.precio_alquiler ?? "") }));
      }
    } catch (e: any) {
      setError(errorMessage(e));
    }
  };

  useEffect(() => { load(); }, [idCuarto]);

  const create = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!idCuarto) { setError("Para crear un alquiler, primero selecciona un cuarto libre."); return; }
    if (!form.id_inquilino) { setError("Selecciona un inquilino antes de guardar el alquiler."); return; }
    try {
      const payload = { ...form, id_inquilino: toNum(form.id_inquilino), id_cuarto: Number(idCuarto), monto_alquiler: toNum(form.monto_alquiler), dia_pago: toNum(form.dia_pago), garantia: toNum(form.garantia), fecha_fin: form.fecha_fin || null, observacion: form.observacion || null };
      await api.post("/api/alquileres", payload);
      setForm({ ...initialForm, id_cuarto: idCuarto });
      await load();
      navigate(`/cuartos/${idCuarto}`);
    } catch (e: any) {
      setError(errorMessage(e));
    }
  };

  const finalizar = async () => {
    if (!confirmId) return;
    try {
      await api.post(`/api/alquileres/${confirmId}/finalizar`);
      setConfirmId(null);
      await load();
    } catch (e: any) {
      setError(errorMessage(e));
    }
  };

  if (!idCuarto) return <div className="page"><PageHeader breadcrumbs={[{ label: "Personas y alquileres" }, { label: "Alquileres" }]} title="Alquileres" description="Consulta contratos. Para crear uno nuevo debes partir desde un cuarto libre." action={<Link className="btn btn-primary" to="/cuartos">Ir a cuartos</Link>} secondaryAction={<button className="btn btn-secondary" onClick={load}>Recargar</button>} /><ErrorMessage message={error}/><ContextHelp message="Para crear un alquiler, primero selecciona un cuarto libre." to="/cuartos" label="Ir a cuartos"/><Card title="Listado de alquileres" description="Contratos registrados y acciones disponibles."><DataTable rows={items} columns={["id_alquiler", "id_inquilino", "id_cuarto", "fecha_inicio", "fecha_fin", "monto_alquiler", "dia_pago", "estado"]} getKey={(r) => r.id_alquiler} emptyState={<EmptyState title="Para crear un alquiler, primero selecciona un cuarto libre." description="Esta vista es de consulta general. Entra a un cuarto libre para crear el contrato." action={<Link className="btn btn-primary" to="/cuartos">Ir a cuartos</Link>} icon="📄" />} actions={(x) => <div className="action-row"><Link className="btn btn-secondary btn-sm" to={`/cuartos/${x.id_cuarto}`}>Ver cuarto</Link><RowActionsMenu items={[{ label: "Finalizar", danger: true, onClick: () => setConfirmId(x.id_alquiler) }]} /></div>} /></Card><ConfirmDialog open={confirmId !== null} title="Finalizar alquiler" message="Esta acción marcará el alquiler como finalizado." danger confirmLabel="Finalizar" onCancel={() => setConfirmId(null)} onConfirm={finalizar} /></div>;

  const libre = String(cuarto?.estado).toLowerCase() === "libre";
  const breadcrumbs: BreadcrumbItem[] = [{ label: "Propiedades", to: "/casas" }, { label: casa?.nombre_casa || `Casa #${cuarto?.id_casa || ""}`, to: cuarto ? `/casas/${cuarto.id_casa}` : undefined }, { label: `Cuarto ${cuarto?.numero_cuarto || `#${idCuarto}`}`, to: `/cuartos/${idCuarto}` }, { label: "Crear alquiler" }];

  return <div className="page"><PageHeader breadcrumbs={breadcrumbs} title="Crear alquiler para este cuarto" description="El cuarto queda definido por el contexto; solo elige inquilino y datos del contrato." action={libre ? <button className="btn btn-primary">+ Crear alquiler</button> : undefined} secondaryAction={<Link className="btn btn-secondary" to={`/cuartos/${idCuarto}`}>Volver al cuarto</Link>} /><ErrorMessage message={error}/><Card title="Contexto seleccionado" description="No necesitas escribir el ID del cuarto."><ContextSummary items={[{ label: "Casa", value: casa?.nombre_casa }, { label: "Cuarto", value: cuarto?.numero_cuarto || idCuarto }, { label: "Estado", value: cuarto?.estado }]} /></Card>{!libre ? <ContextHelp message="Para crear un alquiler, primero selecciona un cuarto libre." to="/cuartos" label="Ir a cuartos"/> : <Drawer open title="Nuevo alquiler" description="El payload mantiene id_cuarto con el valor del cuarto seleccionado." onClose={() => navigate(`/cuartos/${idCuarto}`)} footer={<FormActions formId="alquiler-form" onCancel={() => navigate(`/cuartos/${idCuarto}`)} submitLabel="Guardar alquiler" />}><ContextSummary items={[{ label: "Casa", value: casa?.nombre_casa }, { label: "Cuarto", value: cuarto?.numero_cuarto || idCuarto }, { label: "ID cuarto", value: idCuarto }]} /><form id="alquiler-form" onSubmit={create} className="form-grid" style={{ marginTop: 16 }}><SearchSelect label="Inquilino" items={inquilinos} selectedItem={selectedInquilino} onSelect={(inquilino) => setForm({ ...form, id_inquilino: inquilino ? String(inquilino.id_inquilino) : "" })} getKey={(inquilino) => inquilino.id_inquilino} getOptionLabel={inquilinoLabel} getSelectedLabel={inquilinoSelectedLabel} getSearchText={inquilinoSearchText} placeholder="Buscar por nombre, CI, teléfono o ID..." emptyItemsMessage="Primero registra un inquilino." noResultsMessage="No se encontraron inquilinos." required />{contextFields.map((k) => <FormInput key={k} label={k} required={requiredFields.has(k)} value={form[k]} onChange={(v) => setForm({ ...form, [k]: v })} />)}</form></Drawer>}<Card title="Alquileres de este cuarto" description="Historial filtrado del cuarto seleccionado."><DataTable rows={items.filter((x) => String(x.id_cuarto) === String(idCuarto))} columns={["id_alquiler", "id_inquilino", "fecha_inicio", "fecha_fin", "monto_alquiler", "dia_pago", "estado"]} getKey={(r) => r.id_alquiler} emptyState={<EmptyState title="Este cuarto todavía no tiene alquileres registrados." description="Si está libre, crea el primer alquiler desde el panel lateral." icon="📄" />} actions={(x) => <div className="action-row"><RowActionsMenu items={[{ label: "Finalizar", danger: true, onClick: () => setConfirmId(x.id_alquiler) }]} /></div>} /></Card><ConfirmDialog open={confirmId !== null} title="Finalizar alquiler" message="Esta acción marcará el alquiler como finalizado." danger confirmLabel="Finalizar" onCancel={() => setConfirmId(null)} onConfirm={finalizar} /></div>;
}
