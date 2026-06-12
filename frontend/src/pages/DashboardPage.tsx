import { Link } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { Card, PageHeader } from "../components/ui";

const quickLinks = [
  ["/casas", "Casas", "Registra y organiza las propiedades."],
  ["/cuartos", "Cuartos", "Controla disponibilidad y precios."],
  ["/inquilinos", "Inquilinos", "Administra datos de contacto."],
  ["/alquileres", "Alquileres", "Gestiona contratos activos."],
  ["/cobros", "Cobros", "Genera y revisa cuotas mensuales."],
  ["/reportes", "Reportes", "Consulta resultados por periodo."],
] as const;

export default function DashboardPage(){
  const { user } = useAuth();
  return (
    <div className="page">
      <PageHeader title="Dashboard" description={`Bienvenido${user?.nombre ? `, ${user.nombre}` : ""}. Este es el centro de control para administrar el flujo completo de alquileres.`} />
      <div className="stats-grid">
        <div className="stat-card blue"><span className="stat-label">Módulos activos</span><strong className="stat-value">13</strong></div>
        <div className="stat-card purple"><span className="stat-label">Flujo principal</span><strong className="stat-value">8</strong></div>
        <div className="stat-card green"><span className="stat-label">Sesión</span><strong className="stat-value">OK</strong></div>
        <div className="stat-card orange"><span className="stat-label">Rol actual</span><strong className="stat-value" style={{fontSize:"1.35rem"}}>{user?.rol || "—"}</strong></div>
      </div>
      <Card title="Accesos rápidos" description="Entra directamente a las áreas más usadas del sistema.">
        <div className="quick-grid">
          {quickLinks.map(([to, title, desc]) => <Link key={to} className="quick-link" to={to}><strong>{title}</strong><span>{desc}</span></Link>)}
        </div>
      </Card>
      <Card title="Flujo recomendado" description="Orden sugerido para operar el sistema sin perder consistencia.">
        <div className="flow">
          {['Casas','Cuartos','Inquilinos','Alquileres','Periodos','Servicios','Cobros','Pagos','Reportes'].map((step, index)=>(
            <span key={step} style={{display:'contents'}}><span className="flow-step">{step}</span>{index < 8 && <span className="flow-arrow">→</span>}</span>
          ))}
        </div>
      </Card>
    </div>
  );
}
