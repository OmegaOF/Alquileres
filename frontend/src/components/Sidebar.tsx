import { NavLink } from "react-router-dom";

const links = [
  ["/dashboard", "Dashboard", "▦"],
  ["/usuarios", "Usuarios", "👤"],
  ["/casas", "Casas", "🏠"],
  ["/cuartos", "Cuartos", "🚪"],
  ["/inquilinos", "Inquilinos", "🤝"],
  ["/alquileres", "Alquileres", "📄"],
  ["/periodos", "Periodos", "🗓"],
  ["/servicios", "Servicios", "🧾"],
  ["/servicios-mensuales", "Servicios Mensuales", "💡"],
  ["/cobros", "Cobros", "💰"],
  ["/pagos", "Pagos", "✅"],
  ["/egresos", "Egresos", "📉"],
  ["/reportes", "Reportes", "📊"],
] as const;

export default function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-section-title">Menú principal</div>
      {links.map(([to, label, icon]) => (
        <NavLink key={to} to={to} className={({ isActive }) => `sidebar-link${isActive ? " active" : ""}`}>
          <span className="sidebar-icon">{icon}</span>
          <span>{label}</span>
        </NavLink>
      ))}
    </aside>
  );
}
