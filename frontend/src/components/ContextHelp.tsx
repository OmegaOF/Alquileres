import { Link } from "react-router-dom";
import { Card } from "./ui";

export default function ContextHelp({ message, to, label }: { message: string; to: string; label: string }) {
  return (
    <Card title="Selecciona un contexto" description={message}>
      <Link className="btn btn-primary" to={to}>{label}</Link>
    </Card>
  );
}
