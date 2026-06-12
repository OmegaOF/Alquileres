import { useState } from "react";
import { Navigate, useNavigate } from "react-router-dom";
import api from "../lib/api";
import { useAuth } from "../contexts/AuthContext";
import { ErrorMessage, Field } from "../components/ui";

export default function LoginPage(){
  const { token, login } = useAuth();
  const nav = useNavigate();
  const [correo,setCorreo] = useState("");
  const [password,setPassword] = useState("");
  const [error,setError] = useState("");
  if (token) return <Navigate to="/dashboard" replace />;
  const submit = async (e:React.FormEvent)=>{
    e.preventDefault();
    try{
      setError("");
      const {data} = await api.post('/api/auth/login',{correo,password});
      await login(data.access_token);
      nav('/dashboard');
    }catch(e:any){ setError(e?.response?.data?.detail || 'Credenciales inválidas'); }
  };
  return (
    <div className="login-page">
      <section className="login-hero">
        <div className="brand" style={{ marginBottom: 34 }}><span className="brand-mark">⌂</span><span>Sistema Alquileres</span></div>
        <h1>Administra alquileres con claridad.</h1>
        <p>Un panel simple y ordenado para gestionar casas, cuartos, inquilinos, cobros, pagos y reportes desde un solo lugar.</p>
        <div className="flow" style={{ marginTop: 24 }}>
          {['Casas','Cuartos','Alquileres','Cobros','Pagos'].map((x, i)=>(
            <span key={x} className="flow-step">{i + 1}. {x}</span>
          ))}
        </div>
      </section>
      <section className="login-panel">
        <div className="login-card">
          <p className="eyebrow">Acceso seguro</p>
          <h2>Iniciar sesión</h2>
          <p className="page-description">Ingresa tus credenciales para continuar al panel administrativo.</p>
          <form onSubmit={submit}>
            <ErrorMessage message={error} />
            <Field label="Correo"><input value={correo} onChange={(e)=>setCorreo(e.target.value)} placeholder="correo@ejemplo.com" /></Field>
            <Field label="Contraseña"><input type="password" value={password} onChange={(e)=>setPassword(e.target.value)} placeholder="Tu contraseña" /></Field>
            <button className="btn btn-primary" type="submit">Ingresar al sistema</button>
          </form>
        </div>
      </section>
    </div>
  );
}
