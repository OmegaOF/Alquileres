import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import api from "../lib/api";
import PeriodoActualTabs from "../components/PeriodoActualTabs";
import { BreadcrumbItem, Card, DataTable, EmptyState, ErrorMessage, PageHeader, errorMessage, formatMoney } from "../components/ui";

const meses = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"];

export default function RecordatoriosPage() {
  const { idPeriodo } = useParams();
  const navigate = useNavigate();
  const [periodo, setPeriodo] = useState<any>(null);
  const [items, setItems] = useState<any[]>([]);
  const [error, setError] = useState("");
  const load = async () => {
    try {
      setError("");
      const current = idPeriodo ? (await api.get(`/api/periodos/${idPeriodo}`)).data : (await api.get("/api/periodos/actual")).data;
      if (!idPeriodo) { navigate(`/periodos/${current.id_periodo}/recordatorios`, { replace: true }); return; }
      const { data } = await api.get(`/api/cobros/periodo/${current.id_periodo}/cobranza`);
      setPeriodo(current);
      setItems(data.items || []);
    } catch (e: any) { setError(errorMessage(e)); }
  };
  useEffect(() => { load(); }, [idPeriodo]);
  const preparar = async (r: any, estado = "preparado") => {
    if (!r.id_cobro) return;
    await api.post(`/api/cobros/${r.id_cobro}/recordatorio`, { estado, observacion: estado === "pendiente_confirmar_pago" ? "El inquilino indicó pago; falta confirmar manualmente." : "Contacto registrado manualmente." });
    await load();
  };
  const nombrePeriodo = periodo ? `${meses[periodo.mes]} ${periodo.anio}` : `Periodo #${idPeriodo}`;
  const pendientes = items.filter((x) => Number(x.saldo_pendiente || 0) > 0);
  const pagoReportado = items.filter((x) => x.estado_recordatorio === "pendiente_confirmar_pago");
  const sinRespuesta = items.filter((x) => !x.estado_recordatorio || x.estado_recordatorio === "no_preparado");
  const breadcrumbs: BreadcrumbItem[] = [{ label: "FINANZAS / COBRANZA", to: "/periodos" }, { label: nombrePeriodo, to: `/periodos/${idPeriodo}/trabajo-mensual` }, { label: "Recordatorios" }];
  return <div className="page"><PageHeader breadcrumbs={breadcrumbs} title="Recordatorios" description="Seguimiento operativo interno del periodo. No envía WhatsApp real, no registra pagos y no cambia saldos." action={<Link className="btn btn-primary" to={`/periodos/${idPeriodo}/cobros`}>Ir a pagos / confirmaciones</Link>} secondaryAction={<button className="btn btn-secondary" onClick={load}>Recargar</button>} /><ErrorMessage message={error}/><PeriodoActualTabs idPeriodo={idPeriodo} active="recordatorios" /><Card title="Alcance de esta vista" description="Base futura para WhatsApp; por ahora solo organiza el seguimiento interno."><div className="alert info">Los botones preparan estados operativos: mensaje preparado, pago reportado pendiente de confirmar o sin respuesta. No hacen envíos reales ni modifican la cobranza.</div></Card><div className="stats-grid"><div className="stat-card orange"><span className="stat-label">Contactos pendientes</span><strong className="stat-value">{pendientes.length}</strong></div><div className="stat-card blue"><span className="stat-label">Pago reportado</span><strong className="stat-value">{pagoReportado.length}</strong></div><div className="stat-card purple"><span className="stat-label">Sin respuesta</span><strong className="stat-value">{sinRespuesta.length}</strong></div><div className="stat-card green"><span className="stat-label">Saldo en seguimiento</span><strong className="stat-value">{formatMoney(pendientes.reduce((a, x) => a + Number(x.saldo_pendiente || 0), 0))}</strong></div></div><Card title="Seguimiento operativo" description="Inquilinos/contactos pendientes, mensaje preparado, pagos reportados y pendientes de confirmar."><DataTable rows={items} columns={["inquilino", "casa", "cuarto", "saldo_pendiente", "fecha_limite", "estado_financiero", "estado_recordatorio"]} getKey={(r) => r.id_cobro} emptyState={<EmptyState title="Sin recordatorios del periodo." description="Cuando existan cobros, podrás preparar mensajes o marcar pagos por confirmar." icon="🔔" />} actions={(r) => <div className="action-row"><button className="btn btn-secondary btn-sm" onClick={() => preparar(r)}>Mensaje preparado</button><button className="btn btn-secondary btn-sm" onClick={() => preparar(r, "pendiente_confirmar_pago")}>Marcar pago reportado</button><button className="btn btn-secondary btn-sm" onClick={() => preparar(r, "sin_respuesta")}>Sin respuesta</button></div>} /></Card></div>;
}
