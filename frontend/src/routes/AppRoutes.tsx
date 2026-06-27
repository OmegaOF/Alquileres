import { Navigate, Route, Routes } from "react-router-dom";
import Layout from "../components/Layout";
import ProtectedRoute from "../components/ProtectedRoute";
import LoginPage from "../pages/LoginPage";
import DashboardPage from "../pages/DashboardPage";
import UsuariosPage from "../pages/UsuariosPage";
import CasasPage from "../pages/CasasPage";
import CuartosPage from "../pages/CuartosPage";
import InquilinosPage from "../pages/InquilinosPage";
import AlquileresPage from "../pages/AlquileresPage";
import PeriodosPage from "../pages/PeriodosPage";
import ServiciosPage from "../pages/ServiciosPage";
import ServiciosMensualesPage from "../pages/ServiciosMensualesPage";
import CobrosPage from "../pages/CobrosPage";
import PagosPage from "../pages/PagosPage";
import EgresosPage from "../pages/EgresosPage";
import ReportesPage from "../pages/ReportesPage";
import TrabajoMensualPage from "../pages/TrabajoMensualPage";
import RecordatoriosPage from "../pages/RecordatoriosPage";

const wrap = (el: JSX.Element) => <ProtectedRoute><Layout>{el}</Layout></ProtectedRoute>;

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      <Route path="/dashboard" element={wrap(<DashboardPage />)} />
      <Route path="/usuarios" element={wrap(<UsuariosPage />)} />
      <Route path="/casas" element={wrap(<CasasPage />)} />
      <Route path="/casas/:idCasa" element={wrap(<CasasPage />)} />
      <Route path="/casas/:idCasa/cuartos" element={<Navigate to=".." replace />} />
      <Route path="/casas/:idCasa/cuartos/nuevo" element={wrap(<CuartosPage />)} />
      <Route path="/cuartos" element={<Navigate to="/casas" replace />} />
      <Route path="/cuartos/:idCuarto" element={wrap(<CuartosPage />)} />
      <Route path="/cuartos/:idCuarto/alquileres/nuevo" element={wrap(<AlquileresPage />)} />
      <Route path="/inquilinos" element={wrap(<InquilinosPage />)} />
      <Route path="/alquileres" element={wrap(<AlquileresPage />)} />
      <Route path="/periodos" element={wrap(<PeriodosPage />)} />
      <Route path="/periodo-actual" element={wrap(<TrabajoMensualPage />)} />
      <Route path="/periodos/:idPeriodo/trabajo-mensual" element={wrap(<TrabajoMensualPage />)} />
      <Route path="/periodos/:idPeriodo/servicios-mensuales" element={wrap(<ServiciosMensualesPage />)} />
      <Route path="/periodos/:idPeriodo/cobros" element={wrap(<CobrosPage />)} />
      <Route path="/periodos/:idPeriodo/recordatorios" element={wrap(<RecordatoriosPage />)} />
      <Route path="/periodos/:idPeriodo/reportes" element={wrap(<ReportesPage />)} />
      <Route path="/servicios" element={wrap(<ServiciosPage />)} />
      <Route path="/servicios-mensuales" element={<Navigate to="/periodos" replace />} />
      <Route path="/cobros" element={<Navigate to="/periodos" replace />} />
      <Route path="/cobros/:idCobro/pagos/nuevo" element={wrap(<PagosPage />)} />
      <Route path="/pagos" element={<Navigate to="/periodos" replace />} />
      <Route path="/egresos" element={wrap(<EgresosPage />)} />
      <Route path="/reportes" element={wrap(<ReportesPage />)} />
    </Routes>
  );
}
