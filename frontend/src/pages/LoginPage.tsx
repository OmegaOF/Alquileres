import { useState } from "react";
import { Navigate, useNavigate } from "react-router-dom";
import api from "../lib/api";
import { useAuth } from "../contexts/AuthContext";

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
  return <div style={{maxWidth:360, margin:'80px auto'}}><h2>Login</h2>{error && <p style={{color:'red'}}>{error}</p>}<form onSubmit={submit} style={{display:'grid',gap:8}}><input placeholder='Correo' value={correo} onChange={(e)=>setCorreo(e.target.value)} /><input placeholder='Password' type='password' value={password} onChange={(e)=>setPassword(e.target.value)} /><button type='submit'>Ingresar</button></form></div>;
}
