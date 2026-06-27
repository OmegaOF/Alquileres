import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import api from "../lib/api";
import ContextHelp from "../components/ContextHelp";
import PeriodoActualTabs from "../components/PeriodoActualTabs";
import {
  BreadcrumbItem,
  Card,
  DataTable,
  Drawer,
  EmptyState,
  ErrorMessage,
  PageHeader,
  RowActionsMenu,
  errorMessage,
  formatMoney,
} from "../components/ui";
export default function CobrosPage() {
  const { idPeriodo } = useParams();
  const [items, setItems] = useState<any[]>([]);
  const [error, setError] = useState("");
  const [periodo, setPeriodo] = useState<any>(null);
  const [detalle, setDetalle] = useState<any>(null);
  const load = async () => {
    try {
      setError("");
      if (idPeriodo) {
        const [{ data: c }, { data: p }] = await Promise.all([
          api.get(`/api/cobros/periodo/${idPeriodo}/cobranza`),
          api.get(`/api/periodos/${idPeriodo}`),
        ]);
        setItems(c.items || []);
        setPeriodo(p);
        return;
      }
      const { data } = await api.get("/api/cobros");
      setItems(data);
    } catch (e: any) {
      setError(errorMessage(e));
    }
  };
  useEffect(() => {
    load();
  }, [idPeriodo]);
  const verDetalle = async (id: number) => {
    try {
      const { data } = await api.get(`/api/cobros/${id}/detalles`);
      setDetalle(data);
    } catch (e: any) {
      setError(errorMessage(e));
    }
  };
  const total = items.reduce((acc, x) => acc + Number(x.total_a_pagar || 0), 0);
  const pagado = items.reduce((acc, x) => acc + Number(x.total_pagado || 0), 0);
  const pendiente = items.reduce(
    (acc, x) => acc + Number(x.saldo_pendiente || 0),
    0,
  );
  const breadcrumbs: BreadcrumbItem[] = idPeriodo
    ? [
        { label: "FINANZAS / COBRANZA", to: "/periodos" },
        {
          label: periodo?.nombre_periodo || `Periodo #${idPeriodo}`,
          to: `/periodos/${idPeriodo}/trabajo-mensual`,
        },
        { label: "Pagos / confirmaciones" },
      ]
    : [{ label: "FINANZAS / COBRANZA" }, { label: "Pagos / confirmaciones" }];
  return (
    <div className="page">
      <PageHeader
        breadcrumbs={breadcrumbs}
        title={
          idPeriodo
            ? `Pagos / confirmaciones de ${periodo?.nombre_periodo || `Periodo #${idPeriodo}`}`
            : "Pagos / confirmaciones"
        }
        description={
          idPeriodo
            ? "Vista interna del periodo para revisar cobros generados y registrar pagos."
            : "Entrada general deshabilitada: selecciona un periodo para entrar a pagos / confirmaciones."
        }
        action={
          idPeriodo ? undefined : (
            <Link className="btn btn-primary" to="/periodos">
              Ir a periodos
            </Link>
          )
        }
      />
      <ErrorMessage message={error} />
      {idPeriodo && <PeriodoActualTabs idPeriodo={idPeriodo} active="pagos" />}
      <div className="stats-grid">
        <div className="stat-card blue">
          <span className="stat-label">Registros visibles</span>
          <strong className="stat-value">{items.length}</strong>
        </div>
        <div className="stat-card green">
          <span className="stat-label">Total pagado</span>
          <strong className="stat-value">{formatMoney(pagado)}</strong>
        </div>
        <div className="stat-card purple">
          <span className="stat-label">Total a cobrar</span>
          <strong className="stat-value">{formatMoney(total)}</strong>
        </div>
        <div className="stat-card orange">
          <span className="stat-label">Saldo pendiente</span>
          <strong className="stat-value">{formatMoney(pendiente)}</strong>
        </div>
      </div>
      {!idPeriodo && (
        <ContextHelp
          message="Para revisar pagos / confirmaciones, primero selecciona un periodo."
          to="/periodos"
          label="Ir a periodos"
        />
      )}
      <Card
        title="Pagos / confirmaciones"
        description="Estado financiero de cada cobro generado y acceso al registro de pagos."
      >
        <DataTable
          rows={items}
          columns={
            idPeriodo
              ? [
                  "inquilino",
                  "casa",
                  "cuarto",
                  "modalidad",
                  "concepto_principal",
                  "total_a_pagar",
                  "total_pagado",
                  "saldo_pendiente",
                  "estado_financiero",
                ]
              : ["total_a_pagar", "total_pagado", "saldo_pendiente", "estado"]
          }
          getKey={(r) => r.id_cobro}
          emptyState={
            idPeriodo ? (
              <EmptyState
                title="Este periodo todavía no tiene cobros generados."
                description="Abre la vista de alquileres del periodo para revisar o generar cobros si corresponde."
                action={
                  <Link
                    className="btn btn-primary"
                    to={`/periodos/${idPeriodo}/trabajo-mensual`}
                  >
                    Ir a alquileres
                  </Link>
                }
                icon="💰"
              />
            ) : (
              <EmptyState
                title="No hay registros para mostrar."
                description="Selecciona un periodo para consultar pagos / confirmaciones."
                action={
                  <Link className="btn btn-primary" to="/periodos">
                    Ir a periodos
                  </Link>
                }
                icon="💰"
              />
            )
          }
          actions={(r) => (
            <div className="action-row">
              <Link
                className="btn btn-primary btn-sm"
                to={`/cobros/${r.id_cobro}/pagos/nuevo`}
              >
                Registrar pago
              </Link>
              <RowActionsMenu
                items={[
                  {
                    label: "Ver detalle",
                    onClick: () => verDetalle(r.id_cobro),
                  },
                  {
                    label: "Pagos / confirmaciones",
                    to: `/cobros/${r.id_cobro}/pagos/nuevo`,
                  },
                  {
                    label: "Alquileres",
                    to: `/periodos/${r.id_periodo}/trabajo-mensual`,
                  },
                ]}
              />
            </div>
          )}
        />
      </Card>
      <Drawer
        open={!!detalle}
        title="Detalle del cobro"
        description="Conceptos vigentes del cobro seleccionado."
        onClose={() => setDetalle(null)}
      >
        {detalle && (
          <div className="stack">
            <div className="stats-grid">
              <div className="stat-card purple">
                <span className="stat-label">Total a pagar</span>
                <strong className="stat-value">
                  {formatMoney(detalle.total_a_pagar)}
                </strong>
              </div>
              <div className="stat-card green">
                <span className="stat-label">Total pagado</span>
                <strong className="stat-value">
                  {formatMoney(detalle.total_pagado)}
                </strong>
              </div>
              <div className="stat-card orange">
                <span className="stat-label">Saldo pendiente</span>
                <strong className="stat-value">
                  {formatMoney(detalle.saldo_pendiente)}
                </strong>
              </div>
              <div className="stat-card blue">
                <span className="stat-label">Estado</span>
                <strong className="stat-value">{detalle.estado}</strong>
              </div>
            </div>
            <DataTable
              rows={detalle.detalles || []}
              columns={["tipo_concepto", "concepto", "monto", "descripcion"]}
              getKey={(r) => r.id_detalle}
            />
          </div>
        )}
      </Drawer>
    </div>
  );
}
