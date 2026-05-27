import { NavLink } from "react-router-dom";

const links = [
  ["/dashboard", "Dashboard"],["/usuarios", "Usuarios"],["/casas", "Casas"],["/cuartos", "Cuartos"],
  ["/inquilinos", "Inquilinos"],["/alquileres", "Alquileres"],["/periodos", "Periodos"],["/servicios", "Servicios"],
  ["/servicios-mensuales", "Servicios Mensuales"],["/cobros", "Cobros"],["/pagos", "Pagos"],["/egresos", "Egresos"],["/reportes", "Reportes"],
] as const;

export default function Sidebar() {
  return <aside style={{ minWidth: 220, borderRight: "1px solid #ddd", padding: 12 }}>{links.map(([to,label]) => (
    <div key={to} style={{ marginBottom: 8 }}><NavLink to={to}>{label}</NavLink></div>
  ))}</aside>;
}
