import { Link } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

export default function DashboardPage(){
  const { user } = useAuth();
  return <div>
    <h2>Sistema de Alquileres</h2>
    <p>Usuario autenticado: <strong>{user?.nombre}</strong> ({user?.rol})</p>
    <p>Flujo: casas → cuartos → inquilinos → alquileres → periodos → servicios mensuales → cobros → pagos → reportes</p>
    <div style={{display:'flex', gap:8, flexWrap:'wrap'}}>
      {['/casas','/cuartos','/inquilinos','/alquileres','/periodos','/servicios-mensuales','/cobros','/pagos','/reportes'].map((r)=><Link key={r} to={r}>{r}</Link>)}
    </div>
  </div>;
}
