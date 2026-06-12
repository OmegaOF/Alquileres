import { ReactNode, useEffect, useState } from "react";
import { Link } from "react-router-dom";

const statusClasses: Record<string, string> = {
  activo: "success", activa: "success", inactivo: "neutral", inactiva: "neutral", libre: "success", ocupado: "danger", reservado: "info", mantenimiento: "warning", pendiente: "warning", parcial: "info", pagado: "success", atrasado: "danger", abierto: "success", cerrado: "neutral", finalizado: "neutral", cancelado: "danger", anulado: "danger", valido: "success",
};

export type BreadcrumbItem = { label: string; to?: string };
export type ActionItem = { label: string; to?: string; onClick?: () => void; danger?: boolean; disabled?: boolean };
export type TabItem = { label: string; to?: string; active?: boolean; onClick?: () => void; badge?: ReactNode };

export function formatLabel(value: string) { return value.replace(/_/g, " ").replace(/\b\w/g, (c) => c.toUpperCase()); }
export function formatMoney(value: unknown) { const n = Number(value ?? 0); if (Number.isNaN(n)) return "0.00"; return n.toLocaleString("es-BO", { minimumFractionDigits: 2, maximumFractionDigits: 2 }); }
export function errorMessage(e: any) { return e?.response?.data?.detail ? JSON.stringify(e.response.data.detail) : "Ocurrió un error. Revisa los datos e inténtalo nuevamente."; }

export function StatusBadge({ value }: { value: unknown }) {
  const text = String(value ?? ""); const key = text.toLowerCase(); const tone = statusClasses[key] ?? "primary";
  return <span className={`badge badge-${tone}`}>{text || "Sin estado"}</span>;
}

export function DisplayValue({ name, value }: { name?: string; value: unknown }) {
  const normalized = String(value ?? "").toLowerCase();
  if ((name && name.toLowerCase().includes("estado")) || statusClasses[normalized]) return <StatusBadge value={value} />;
  if (value === null || value === undefined || value === "") return <span style={{ color: "#98a2b3" }}>—</span>;
  return <>{String(value)}</>;
}

export function Breadcrumbs({ items }: { items?: BreadcrumbItem[] }) {
  if (!items?.length) return null;
  return <nav className="breadcrumbs" aria-label="Ruta visual">{items.map((item, index) => <span className="breadcrumb-item" key={`${item.label}-${index}`}>{item.to && index < items.length - 1 ? <Link to={item.to}>{item.label}</Link> : <span>{item.label}</span>}{index < items.length - 1 && <span className="breadcrumb-separator">/</span>}</span>)}</nav>;
}

export function PageActions({ primary, secondary }: { primary?: ReactNode; secondary?: ReactNode }) {
  if (!primary && !secondary) return null;
  return <div className="page-actions">{secondary}<>{primary}</></div>;
}

export function PageHeader({ title, description, action, secondaryAction, breadcrumbs }: { title: string; description: string; action?: ReactNode; secondaryAction?: ReactNode; breadcrumbs?: BreadcrumbItem[] }) {
  return <div className="page-heading"><Breadcrumbs items={breadcrumbs} /><div className="page-header"><div><p className="eyebrow">Panel administrativo</p><h1 className="page-title">{title}</h1><p className="page-description">{description}</p></div><PageActions primary={action} secondary={secondaryAction} /></div></div>;
}

export function Card({ title, description, children, action }: { title?: string; description?: string; children: ReactNode; action?: ReactNode }) {
  return <section className="card">{(title || description || action) && <div className="card-header"><div>{title && <h2 className="card-title">{title}</h2>}{description && <p className="card-description">{description}</p>}</div>{action}</div>}<div className="card-body">{children}</div></section>;
}

export function Field({ label, children }: { label: string; children: ReactNode }) { return <div className="field"><label>{label}</label>{children}</div>; }
export function FormInput({ label, value, onChange, type = "text" }: { label: string; value: any; onChange: (v: string) => void; type?: string }) { return <Field label={formatLabel(label)}><input type={type} value={value ?? ""} placeholder={formatLabel(label)} onChange={(e) => onChange(e.target.value)} /></Field>; }
export function ErrorMessage({ message }: { message: string }) { if (!message) return null; return <div className="error-message">{message}</div>; }

export function EmptyState({ title = "No hay registros para mostrar.", description, action, secondaryAction, icon = "✨" }: { title?: string; description?: string; action?: ReactNode; secondaryAction?: ReactNode; icon?: ReactNode }) {
  return <div className="empty-state rich"><div className="empty-icon">{icon}</div><h3>{title}</h3>{description && <p>{description}</p>} {(action || secondaryAction) && <div className="empty-actions">{action}{secondaryAction}</div>}</div>;
}

export function DataTable({ rows, columns, getKey, actions, emptyState }: { rows: any[]; columns: string[]; getKey?: (row: any, index: number) => string | number; actions?: (row: any) => ReactNode; emptyState?: ReactNode }) {
  if (rows.length === 0 && emptyState) return <>{emptyState}</>;
  return <div className="table-wrap"><table className="data-table"><thead><tr>{columns.map((c) => <th key={c}>{formatLabel(c)}</th>)}{actions && <th>Acciones</th>}</tr></thead><tbody>{rows.length === 0 ? <tr><td colSpan={columns.length + (actions ? 1 : 0)}><EmptyState /></td></tr> : rows.map((row, index) => <tr key={getKey ? getKey(row, index) : index}>{columns.map((c) => <td key={c}><DisplayValue name={c} value={row[c]} /></td>)}{actions && <td className="actions-cell">{actions(row)}</td>}</tr>)}</tbody></table></div>;
}

export function Modal({ open, title, description, children, footer, onClose }: { open: boolean; title: string; description?: string; children: ReactNode; footer?: ReactNode; onClose: () => void }) {
  useEffect(() => { if (!open) return; const onKey = (e: KeyboardEvent) => e.key === "Escape" && onClose(); window.addEventListener("keydown", onKey); return () => window.removeEventListener("keydown", onKey); }, [open, onClose]);
  if (!open) return null;
  return <div className="overlay"><button className="overlay-backdrop" aria-label="Cerrar" onClick={onClose} /><section className="modal-panel" role="dialog" aria-modal="true"><header className="surface-header"><div><h2>{title}</h2>{description && <p>{description}</p>}</div><button className="icon-btn" onClick={onClose} aria-label="Cerrar">×</button></header><div className="surface-body">{children}</div>{footer && <footer className="surface-footer">{footer}</footer>}</section></div>;
}

export function Drawer({ open, title, description, children, footer, onClose }: { open: boolean; title: string; description?: string; children: ReactNode; footer?: ReactNode; onClose: () => void }) {
  useEffect(() => { if (!open) return; const onKey = (e: KeyboardEvent) => e.key === "Escape" && onClose(); window.addEventListener("keydown", onKey); return () => window.removeEventListener("keydown", onKey); }, [open, onClose]);
  if (!open) return null;
  return <div className="overlay"><button className="overlay-backdrop" aria-label="Cerrar" onClick={onClose} /><aside className="drawer-panel" role="dialog" aria-modal="true"><header className="surface-header"><div><h2>{title}</h2>{description && <p>{description}</p>}</div><button className="icon-btn" onClick={onClose} aria-label="Cerrar">×</button></header><div className="surface-body">{children}</div>{footer && <footer className="surface-footer">{footer}</footer>}</aside></div>;
}

export function FormActions({ onCancel, submitLabel = "Guardar", cancelLabel = "Cancelar", formId }: { onCancel: () => void; submitLabel?: string; cancelLabel?: string; formId?: string }) {
  return <div className="form-actions modal-actions"><button className="btn btn-secondary" type="button" onClick={onCancel}>{cancelLabel}</button><button className="btn btn-primary" type="submit" form={formId}>{submitLabel}</button></div>;
}

export function ConfirmDialog({ open, title, message, confirmLabel = "Confirmar", cancelLabel = "Cancelar", danger, onConfirm, onCancel }: { open: boolean; title: string; message: string; confirmLabel?: string; cancelLabel?: string; danger?: boolean; onConfirm: () => void; onCancel: () => void }) {
  return <Modal open={open} title={title} description={message} onClose={onCancel} footer={<div className="form-actions modal-actions"><button className="btn btn-secondary" onClick={onCancel}>{cancelLabel}</button><button className={`btn ${danger ? "btn-danger" : "btn-primary"}`} onClick={onConfirm}>{confirmLabel}</button></div>}><div className="confirm-icon">{danger ? "⚠️" : "✓"}</div></Modal>;
}

export function ContextSummary({ items }: { items: { label: string; value: ReactNode }[] }) {
  return <div className="context-summary">{items.map((item) => <div key={item.label}><strong>{item.label}</strong><span>{item.value || "—"}</span></div>)}</div>;
}

export function RowActionsMenu({ items }: { items: ActionItem[] }) {
  const [open, setOpen] = useState(false); const enabled = items.filter((i) => !i.disabled);
  if (!enabled.length) return null;
  return <div className="row-menu"><button className="row-menu-trigger" onClick={() => setOpen(!open)} aria-label="Más acciones">⋮</button>{open && <div className="row-menu-panel">{enabled.map((item) => item.to ? <Link key={item.label} to={item.to} className={`row-menu-item${item.danger ? " danger" : ""}`} onClick={() => setOpen(false)}>{item.label}</Link> : <button key={item.label} className={`row-menu-item${item.danger ? " danger" : ""}`} onClick={() => { setOpen(false); item.onClick?.(); }}>{item.label}</button>)}</div>}</div>;
}

export function Tabs({ items }: { items: TabItem[] }) {
  return <div className="tabs" role="tablist">{items.map((item) => item.to ? <Link key={item.label} to={item.to} className={`tab${item.active ? " active" : ""}`}>{item.label}{item.badge}</Link> : <button key={item.label} className={`tab${item.active ? " active" : ""}`} onClick={item.onClick}>{item.label}{item.badge}</button>)}</div>;
}
