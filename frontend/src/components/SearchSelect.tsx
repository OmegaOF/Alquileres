import { useMemo, useState } from "react";
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
}: SearchSelectProps<T>) {
  const [query, setQuery] = useState("");
  const normalizedQuery = query.trim().toLowerCase();
  const filteredItems = useMemo(() => {
    if (!normalizedQuery) return items;
    return items.filter((item) => {
      const searchable = getSearchText ? getSearchText(item) : getOptionLabel(item);
      return searchable.toLowerCase().includes(normalizedQuery);
    });
  }, [getOptionLabel, getSearchText, items, normalizedQuery]);

  const hasItems = items.length > 0;

  return (
    <Field label={label}>
      <div className="search-select">
        <input
          type="search"
          value={query}
          placeholder={placeholder}
          onChange={(e) => setQuery(e.target.value)}
        />
        <div className="search-select-results" role="listbox" aria-label={label}>
          {!hasItems ? (
            <div className="search-select-message">{emptyItemsMessage}</div>
          ) : filteredItems.length === 0 ? (
            <div className="search-select-message">{noResultsMessage}</div>
          ) : (
            filteredItems.map((item) => {
              const key = getKey(item);
              const selected = selectedItem ? String(getKey(selectedItem)) === String(key) : false;
              return (
                <button
                  type="button"
                  className={`search-select-option${selected ? " selected" : ""}`}
                  key={key}
                  onClick={() => { onSelect(item); setQuery(""); }}
                >
                  {getOptionLabel(item)}
                </button>
              );
            })
          )}
        </div>
        {selectedItem && (
          <div className="search-select-selected">
            <strong>Seleccionado:</strong> {getSelectedLabel ? getSelectedLabel(selectedItem) : getOptionLabel(selectedItem)}
            <button type="button" onClick={() => onSelect(null)}>Quitar</button>
          </div>
        )}
      </div>
    </Field>
  );
}
