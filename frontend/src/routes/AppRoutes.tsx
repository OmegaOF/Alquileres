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

const wrap = (el: JSX.Element) => <ProtectedRoute><Layout>{el}</Layout></ProtectedRoute>;

export default function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/" element={<Navigate to="/dashboard" replace />} />
      <Route path="/dashboard" element={wrap(<DashboardPage />)} />
      <Route path="/usuarios" element={wrap(<UsuariosPage />)} />
      <Route path="/casas" element={wrap(<CasasPage />)} />
      <Route path="/cuartos" element={wrap(<CuartosPage />)} />
      <Route path="/inquilinos" element={wrap(<InquilinosPage />)} />
      <Route path="/alquileres" element={wrap(<AlquileresPage />)} />
      <Route path="/periodos" element={wrap(<PeriodosPage />)} />
      <Route path="/servicios" element={wrap(<ServiciosPage />)} />
      <Route path="/servicios-mensuales" element={wrap(<ServiciosMensualesPage />)} />
      <Route path="/cobros" element={wrap(<CobrosPage />)} />
      <Route path="/pagos" element={wrap(<PagosPage />)} />
      <Route path="/egresos" element={wrap(<EgresosPage />)} />
      <Route path="/reportes" element={wrap(<ReportesPage />)} />
    </Routes>
  );
}
