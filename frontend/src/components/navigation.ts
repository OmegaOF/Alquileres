export type NavItem = { to: string; label: string; icon: string };
export type NavGroup = { title: string; icon: string; links: NavItem[] };

export const navGroups: NavGroup[] = [
  { title: "INICIO", icon: "▦", links: [{ to: "/dashboard", label: "Dashboard", icon: "▦" }] },
  { title: "INMUEBLES", icon: "🏠", links: [{ to: "/casas", label: "Casas", icon: "🏠" }] },
  { title: "ALQUILERES", icon: "🤝", links: [{ to: "/inquilinos", label: "Inquilinos", icon: "🤝" }, { to: "/alquileres", label: "Alquileres", icon: "📄" }] },
  { title: "FINANZAS / COBRANZA", icon: "🗓", links: [{ to: "/periodo-actual", label: "Periodo actual", icon: "🗓" }, { to: "/periodos", label: "Periodos", icon: "🗓" }, { to: "/egresos", label: "Egresos", icon: "📉" }] },
  { title: "REPORTES", icon: "📊", links: [{ to: "/reportes", label: "Reportes", icon: "📊" }] },
  { title: "CONFIGURACIÓN", icon: "⚙️", links: [{ to: "/servicios", label: "Servicios", icon: "🧾" }, { to: "/usuarios", label: "Usuarios", icon: "👤" }] },
];
