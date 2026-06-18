import { useEffect, useMemo, useRef, useState } from "react";
import { Field } from "./ui";

type SearchSelectProps<T> = {
  label: string;
  items: T[];
  selectedItem: T | null;
  onSelect: (item: T | null) => void;
  getKey: (item: T) => string | number;
  getOptionLabel: (item: T) => string;
  getSelectedLabel?: (item: T) => string;
  getSearchText?: (item: T) => string;
  placeholder?: string;
  emptyItemsMessage?: string;
  noResultsMessage?: string;
  required?: boolean;
  disabled?: boolean;
  disabledMessage?: string;
  selectedLabelPrefix?: string;
};

export default function SearchSelect<T>({
  label,
  items,
  selectedItem,
  onSelect,
  getKey,
  getOptionLabel,
  getSelectedLabel,
  getSearchText,
  placeholder = "Buscar...",
  emptyItemsMessage = "No hay opciones registradas.",
  noResultsMessage = "No se encontraron resultados.",
  required = false,
  disabled = false,
  disabledMessage = "Selecciona primero el contexto requerido.",
  selectedLabelPrefix = "Registro seleccionado:",
}: SearchSelectProps<T>) {
  const [query, setQuery] = useState("");
  const [isOpen, setIsOpen] = useState(false);
  const containerRef = useRef<HTMLDivElement>(null);

  const normalizedQuery = query.trim().toLowerCase();
  const filteredItems = useMemo(() => {
    if (!normalizedQuery) return items.slice(0, 5);
    return items.filter((item) => {
      const searchable = getSearchText ? getSearchText(item) : getOptionLabel(item);
      return searchable.toLowerCase().includes(normalizedQuery);
    });
  }, [getOptionLabel, getSearchText, items, normalizedQuery]);

  useEffect(() => {
    const closeOnClickOutside = (event: MouseEvent) => {
      if (!containerRef.current?.contains(event.target as Node)) setIsOpen(false);
    };

    const closeOnEscape = (event: KeyboardEvent) => {
      if (event.key === "Escape") setIsOpen(false);
    };

    document.addEventListener("mousedown", closeOnClickOutside);
    document.addEventListener("keydown", closeOnEscape);
    return () => {
      document.removeEventListener("mousedown", closeOnClickOutside);
      document.removeEventListener("keydown", closeOnEscape);
    };
  }, []);

  const hasItems = items.length > 0;
  const showResults = isOpen && !selectedItem && !disabled;
  const selectedLabel = selectedItem ? (getSelectedLabel ? getSelectedLabel(selectedItem) : getOptionLabel(selectedItem)) : "";

  return (
    <Field label={label} required={required}>
      <div className="search-select" ref={containerRef}>
        {selectedItem ? (
          <div className="search-select-selected" aria-live="polite">
            <span className="search-select-selected-label">{selectedLabelPrefix}</span>
            <strong>{selectedLabel}</strong>
            <div className="search-select-selected-actions">
              <button
                type="button"
                disabled={disabled}
                onClick={() => {
                  if (disabled) return;
                  onSelect(null);
                  setQuery("");
                  setIsOpen(true);
                }}
              >
                Cambiar
              </button>
              <button
                type="button"
                disabled={disabled}
                onClick={() => {
                  if (disabled) return;
                  onSelect(null);
                  setQuery("");
                  setIsOpen(false);
                }}
              >
                Quitar
              </button>
            </div>
          </div>
        ) : (
          <div className="search-select-control">
            <input
              type="search"
              value={query}
              placeholder={placeholder}
              autoComplete="off"
              aria-expanded={showResults}
              aria-controls={`${label}-results`}
              disabled={disabled}
              onFocus={() => !disabled && setIsOpen(true)}
              onChange={(e) => {
                setQuery(e.target.value);
                setIsOpen(!disabled);
              }}
            />
            {disabled && <div className="search-select-message">{disabledMessage}</div>}
            {showResults && (
              <div className="search-select-results" id={`${label}-results`} role="listbox" aria-label={label}>
                {!hasItems ? (
                  <div className="search-select-message">{emptyItemsMessage}</div>
                ) : filteredItems.length === 0 ? (
                  <div className="search-select-message">{noResultsMessage}</div>
                ) : (
                  filteredItems.map((item) => {
                    const key = getKey(item);
                    return (
                      <button
                        type="button"
                        className="search-select-option"
                        key={key}
                        onClick={() => {
                          onSelect(item);
                          setQuery("");
                          setIsOpen(false);
                        }}
                      >
                        {getOptionLabel(item)}
                      </button>
                    );
                  })
                )}
              </div>
            )}
          </div>
        )}
      </div>
    </Field>
  );
}
