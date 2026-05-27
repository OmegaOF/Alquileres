import { useAuth } from "../contexts/AuthContext";

export default function Navbar() {
  const { user, logout } = useAuth();
  return (
    <header style={{ display: "flex", justifyContent: "space-between", padding: 12, background: "#f0f0f0" }}>
      <strong>Sistema Alquileres</strong>
      <div style={{ display: "flex", gap: 12, alignItems: "center" }}>
        <span>{user?.nombre} ({user?.rol})</span>
        <button onClick={logout}>Cerrar sesión</button>
      </div>
    </header>
  );
}
