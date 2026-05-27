import { BrowserRouter } from "react-router-dom";
import AppRoutes from "./routes/AppRoutes";
import { AuthProvider } from "./contexts/AuthContext";
export default function App(){return <BrowserRouter><AuthProvider><AppRoutes/></AuthProvider></BrowserRouter>}
