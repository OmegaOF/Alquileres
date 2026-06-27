import { Tabs } from "./ui";

export type PeriodoTab = "cobranza" | "servicios" | "pagos" | "recordatorios";

export default function PeriodoActualTabs({ idPeriodo, active }: { idPeriodo: string | number | undefined; active: PeriodoTab }) {
  if (!idPeriodo) return null;
  return <Tabs items={[
    { label: "Alquileres", to: `/periodos/${idPeriodo}/trabajo-mensual`, active: active === "cobranza" },
    { label: "Servicios", to: `/periodos/${idPeriodo}/servicios-mensuales`, active: active === "servicios" },
    { label: "Pagos / confirmaciones", to: `/periodos/${idPeriodo}/cobros`, active: active === "pagos" },
    { label: "Recordatorios", to: `/periodos/${idPeriodo}/recordatorios`, active: active === "recordatorios" },
  ]} />;
}
