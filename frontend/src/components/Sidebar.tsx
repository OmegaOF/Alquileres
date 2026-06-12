import { NavLink } from "react-router-dom";

const groups = [
  { title: "Dashboard", links: [["/dashboard", "Dashboard", "▦"]] },
  { title: "Propiedades", links: [["/casas", "Casas", "🏠"], ["/cuartos", "Cuartos", "🚪"], ["/egresos", "Egresos", "📉"]] },
  { title: "Personas y alquileres", links: [["/inquilinos", "Inquilinos", "🤝"], ["/alquileres", "Alquileres", "📄"]] },
  { title: "Gestión mensual", links: [["/periodos", "Periodos", "🗓"], ["/servicios-mensuales", "Servicios mensuales", "💡"], ["/cobros", "Cobros", "💰"], ["/pagos", "Pagos", "✅"]] },
  { title: "Reportes", links: [["/reportes", "Reportes", "📊"]] },
  { title: "Configuración", links: [["/usuarios", "Usuarios", "👤"], ["/servicios", "Servicios", "🧾"]] },
] as const;

export default function Sidebar() {
  return (
    <aside className="sidebar">
      {groups.map((group) => (
        <div className="sidebar-group" key={group.title}>
          <div className="sidebar-section-title">{group.title}</div>
          {group.links.map(([to, label, icon]) => (
            <NavLink key={to} to={to} className={({ isActive }) => `sidebar-link${isActive ? " active" : ""}`}>
              <span className="sidebar-icon">{icon}</span>
              <span>{label}</span>
            </NavLink>
          ))}
        </div>
      ))}
    </aside>
  );
}
