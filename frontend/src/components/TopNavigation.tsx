import { useEffect, useMemo, useState } from "react";
import { Link, NavLink, useLocation } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { navGroups, NavGroup } from "./navigation";

function pathInGroup(pathname: string, group: NavGroup) {
  return group.links.some((link) => pathname === link.to || pathname.startsWith(`${link.to}/`) || (link.to === "/periodos" && pathname.startsWith("/periodos/")) || (link.to === "/casas" && pathname.startsWith("/casas/")) || (link.to === "/cuartos" && pathname.startsWith("/cuartos/")) || (link.to === "/cobros" && pathname.startsWith("/cobros/")));
}

export default function TopNavigation() {
  const { user, logout } = useAuth();
  const location = useLocation();
  const [openGroup, setOpenGroup] = useState<string | null>(null);
  const [mobileOpen, setMobileOpen] = useState(false);
  const [mobileGroups, setMobileGroups] = useState<Record<string, boolean>>({});

  useEffect(() => { setOpenGroup(null); setMobileOpen(false); }, [location.pathname]);
  useEffect(() => {
    const onKey = (event: KeyboardEvent) => { if (event.key === "Escape") { setOpenGroup(null); setMobileOpen(false); } };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, []);

  const activeGroup = useMemo(() => navGroups.find((group) => pathInGroup(location.pathname, group))?.title, [location.pathname]);

  return (
    <>
      <header className="topbar">
        <Link to="/dashboard" className="brand" aria-label="Sistema de Alquileres">
          <span className="brand-mark">⌂</span>
          <span className="brand-text">Sistema de Alquileres</span>
        </Link>
        <nav className="desktop-nav" aria-label="Navegación principal">
          {navGroups.map((group) => {
            const isActive = activeGroup === group.title;
            const single = group.links.length === 1;
            if (single) {
              const link = group.links[0];
              return <NavLink key={group.title} to={link.to} className={({ isActive: linkActive }) => `top-nav-link${linkActive ? " active" : ""}`}>{group.title}</NavLink>;
            }
            return (
              <div key={group.title} className="top-nav-group">
                <button className={`top-nav-trigger${isActive ? " active" : ""}`} onClick={() => setOpenGroup(openGroup === group.title ? null : group.title)} aria-expanded={openGroup === group.title}>
                  {group.title} <span aria-hidden>⌄</span>
                </button>
                {openGroup === group.title && (
                  <div className="dropdown-panel">
                    {group.links.map((link) => (
                      <NavLink key={link.to} to={link.to} className={({ isActive }) => `dropdown-item${isActive || location.pathname.startsWith(`${link.to}/`) ? " active" : ""}`}>
                        <span>{link.icon}</span><span>{link.label}</span>
                      </NavLink>
                    ))}
                  </div>
                )}
              </div>
            );
          })}
        </nav>
        <div className="topbar-user">
          <div className="user-pill"><strong>{user?.nombre || "Usuario"}</strong><span>{user?.rol || "sesión activa"}</span></div>
          <button className="btn btn-secondary btn-sm desktop-logout" onClick={logout}>Cerrar sesión</button>
          <button className="hamburger" onClick={() => setMobileOpen(true)} aria-label="Abrir menú"><span></span><span></span><span></span></button>
        </div>
      </header>
      {openGroup && <button className="nav-scrim" aria-label="Cerrar menú" onClick={() => setOpenGroup(null)} />}
      {mobileOpen && <div className="mobile-menu-backdrop" onClick={() => setMobileOpen(false)} />}
      <aside className={`mobile-menu${mobileOpen ? " open" : ""}`} aria-hidden={!mobileOpen}>
        <div className="mobile-menu-header"><div className="brand"><span className="brand-mark">⌂</span><span>Sistema de Alquileres</span></div><button className="icon-btn" onClick={() => setMobileOpen(false)} aria-label="Cerrar menú">×</button></div>
        <div className="mobile-user-card"><strong>{user?.nombre || "Usuario"}</strong><span>{user?.rol || "sesión activa"}</span></div>
        <nav className="mobile-nav" aria-label="Navegación móvil">
          {navGroups.map((group) => {
            const expanded = mobileGroups[group.title] ?? activeGroup === group.title;
            return <div className="mobile-nav-group" key={group.title}>
              <button className={`mobile-nav-trigger${activeGroup === group.title ? " active" : ""}`} onClick={() => setMobileGroups((prev) => ({...prev, [group.title]: !expanded}))}><span>{group.icon} {group.title}</span><span>{expanded ? "−" : "+"}</span></button>
              {expanded && <div className="mobile-nav-links">{group.links.map((link) => <NavLink key={link.to} to={link.to} className={({ isActive }) => `mobile-nav-link${isActive || location.pathname.startsWith(`${link.to}/`) ? " active" : ""}`}><span>{link.icon}</span>{link.label}</NavLink>)}</div>}
            </div>;
          })}
        </nav>
        <button className="btn btn-danger mobile-logout" onClick={logout}>Cerrar sesión</button>
      </aside>
    </>
  );
}
