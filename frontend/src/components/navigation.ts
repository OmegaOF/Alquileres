export type NavItem = { to: string; label: string; icon: string };
export type NavGroup = { title: string; icon: string; links: NavItem[] };

export const navGroups: NavGroup[] = [
  { title: "Dashboard", icon: "▦", links: [{ to: "/dashboard", label: "Dashboard", icon: "▦" }] },
  { title: "Propiedades", icon: "🏠", links: [{ to: "/casas", label: "Casas", icon: "🏠" }, { to: "/cuartos", label: "Cuartos", icon: "🚪" }, { to: "/egresos", label: "Egresos", icon: "📉" }] },
  { title: "Personas y alquileres", icon: "🤝", links: [{ to: "/inquilinos", label: "Inquilinos", icon: "🤝" }, { to: "/alquileres", label: "Alquileres", icon: "📄" }] },
  { title: "Gestión mensual", icon: "🗓", links: [{ to: "/periodos", label: "Periodos", icon: "🗓" }, { to: "/servicios-mensuales", label: "Servicios mensuales", icon: "💡" }, { to: "/cobros", label: "Cobros", icon: "💰" }, { to: "/pagos", label: "Pagos", icon: "✅" }] },
  { title: "Reportes", icon: "📊", links: [{ to: "/reportes", label: "Reportes", icon: "📊" }] },
  { title: "Configuración", icon: "⚙️", links: [{ to: "/usuarios", label: "Usuarios", icon: "👤" }, { to: "/servicios", label: "Servicios", icon: "🧾" }] },
];
