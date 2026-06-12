import { Link } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { Card, PageHeader } from "../components/ui";

const areas = [
  { to: "/casas", title: "Propiedades", desc: "Casas, cuartos relacionados y egresos por propiedad.", icon: "🏠" },
  { to: "/inquilinos", title: "Personas y alquileres", desc: "Inquilinos y contratos creados desde un cuarto libre.", icon: "🤝" },
  { to: "/periodos", title: "Gestión mensual", desc: "Periodos como centro de servicios, cobros y pagos.", icon: "🗓" },
  { to: "/reportes", title: "Reportes", desc: "Resultados financieros generales o por periodo.", icon: "📊" },
  { to: "/servicios", title: "Configuración", desc: "Usuarios y catálogo de servicios reutilizables.", icon: "⚙️" },
] as const;

export default function DashboardPage(){
  const { user } = useAuth();
  return (
    <div className="page">
      <PageHeader breadcrumbs={[{ label: "Dashboard" }]} title="Dashboard" description={`Bienvenido${user?.nombre ? `, ${user.nombre}` : ""}. El sistema está organizado por áreas para guiarte sin memorizar el flujo completo.`} />
      <div className="stats-grid">
        <div className="stat-card blue"><span className="stat-label">Áreas de trabajo</span><strong className="stat-value">5</strong></div>
        <div className="stat-card purple"><span className="stat-label">Contexto principal</span><strong className="stat-value" style={{fontSize:"1.35rem"}}>Guiado</strong></div>
        <div className="stat-card green"><span className="stat-label">Sesión</span><strong className="stat-value">OK</strong></div>
        <div className="stat-card orange"><span className="stat-label">Rol actual</span><strong className="stat-value" style={{fontSize:"1.35rem"}}>{user?.rol || "—"}</strong></div>
      </div>
      <Card title="Áreas del sistema" description="Empieza por el área que corresponde a tu tarea y usa las acciones contextuales.">
        <div className="quick-grid">
          {areas.map((area) => <Link key={area.to} className="quick-link" to={area.to}><strong>{area.icon} {area.title}</strong><span>{area.desc}</span></Link>)}
        </div>
      </Card>
      <Card title="Flujos guiados" description="Las acciones principales ahora parten desde la entidad padre correcta.">
        <div className="flow"><span className="flow-step">Casa</span><span className="flow-arrow">→</span><span className="flow-step">Cuartos de esa casa</span><span className="flow-arrow">→</span><span className="flow-step">Cuarto libre</span><span className="flow-arrow">→</span><span className="flow-step">Alquiler</span></div>
        <div className="flow" style={{marginTop:12}}><span className="flow-step">Periodo</span><span className="flow-arrow">→</span><span className="flow-step">Trabajo mensual</span><span className="flow-arrow">→</span><span className="flow-step">Cobros</span><span className="flow-arrow">→</span><span className="flow-step">Pagos y reportes</span></div>
      </Card>
    </div>
  );
}
