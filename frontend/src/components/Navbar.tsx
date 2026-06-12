import { useAuth } from "../contexts/AuthContext";

export default function Navbar() {
  const { user, logout } = useAuth();
  return (
    <header className="navbar">
      <div className="brand">
        <span className="brand-mark">⌂</span>
        <span>Sistema Alquileres</span>
      </div>
      <div className="nav-user">
        <div className="user-pill">
          <strong>{user?.nombre || "Usuario"}</strong>
          <span>{user?.rol || "sesión activa"}</span>
        </div>
        <button className="btn btn-secondary btn-sm" onClick={logout}>Cerrar sesión</button>
      </div>
    </header>
  );
}
