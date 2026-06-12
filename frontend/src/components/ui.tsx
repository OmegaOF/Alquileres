import { ReactNode } from "react";

const statusClasses: Record<string, string> = {
  activo: "success",
  activa: "success",
  inactivo: "neutral",
  inactiva: "neutral",
  libre: "success",
  ocupado: "danger",
  reservado: "info",
  mantenimiento: "warning",
  pendiente: "warning",
  parcial: "info",
  pagado: "success",
  atrasado: "danger",
  abierto: "success",
  cerrado: "neutral",
  finalizado: "neutral",
  cancelado: "danger",
  anulado: "danger",
  valido: "success",
};

export function formatLabel(value: string) {
  return value.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase());
}

export function formatMoney(value: unknown) {
  const n = Number(value ?? 0);
  if (Number.isNaN(n)) return "0.00";
  return n.toLocaleString("es-BO", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

export function errorMessage(e: any) {
  return e?.response?.data?.detail ? JSON.stringify(e.response.data.detail) : "Ocurrió un error. Revisa los datos e inténtalo nuevamente.";
}

export function StatusBadge({ value }: { value: unknown }) {
  const text = String(value ?? "");
  const key = text.toLowerCase();
  const tone = statusClasses[key] ?? "primary";
  return <span className={`badge badge-${tone}`}>{text || "Sin estado"}</span>;
}

export function DisplayValue({ name, value }: { name?: string; value: unknown }) {
  const normalized = String(value ?? "").toLowerCase();
  if ((name && name.toLowerCase().includes("estado")) || statusClasses[normalized]) {
    return <StatusBadge value={value} />;
  }
  if (value === null || value === undefined || value === "") return <span style={{ color: "#98a2b3" }}>—</span>;
  return <>{String(value)}</>;
}

export function PageHeader({ title, description, action }: { title: string; description: string; action?: ReactNode }) {
  return (
    <div className="page-header">
      <div>
        <p className="eyebrow">Panel administrativo</p>
        <h1 className="page-title">{title}</h1>
        <p className="page-description">{description}</p>
      </div>
      {action}
    </div>
  );
}

export function Card({ title, description, children, action }: { title?: string; description?: string; children: ReactNode; action?: ReactNode }) {
  return (
    <section className="card">
      {(title || description || action) && (
        <div className="card-header">
          <div>
            {title && <h2 className="card-title">{title}</h2>}
            {description && <p className="card-description">{description}</p>}
          </div>
          {action}
        </div>
      )}
      <div className="card-body">{children}</div>
    </section>
  );
}

export function Field({ label, children }: { label: string; children: ReactNode }) {
  return <div className="field"><label>{label}</label>{children}</div>;
}

export function FormInput({ label, value, onChange, type = "text" }: { label: string; value: any; onChange: (v: string) => void; type?: string }) {
  return <Field label={formatLabel(label)}><input type={type} value={value ?? ""} placeholder={formatLabel(label)} onChange={(e) => onChange(e.target.value)} /></Field>;
}

export function ErrorMessage({ message }: { message: string }) {
  if (!message) return null;
  return <div className="error-message">{message}</div>;
}

export function DataTable({ rows, columns, getKey, actions }: { rows: any[]; columns: string[]; getKey?: (row: any, index: number) => string | number; actions?: (row: any) => ReactNode }) {
  return (
    <div className="table-wrap">
      <table className="data-table">
        <thead>
          <tr>
            {columns.map((c) => <th key={c}>{formatLabel(c)}</th>)}
            {actions && <th>Acciones</th>}
          </tr>
        </thead>
        <tbody>
          {rows.length === 0 ? (
            <tr><td colSpan={columns.length + (actions ? 1 : 0)}><div className="empty-state">No hay registros para mostrar.</div></td></tr>
          ) : rows.map((row, index) => (
            <tr key={getKey ? getKey(row, index) : index}>
              {columns.map((c) => <td key={c}><DisplayValue name={c} value={row[c]} /></td>)}
              {actions && <td>{actions(row)}</td>}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
