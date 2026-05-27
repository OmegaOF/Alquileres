# Sistema de Alquileres (Monolito Modular)

Proyecto full-stack para administrar casas, cuartos, inquilinos, alquileres, servicios, cobros, pagos y egresos.

## Estructura

- `backend/`: API REST con FastAPI + SQLAlchemy + JWT.
- `frontend/`: SPA con React + Vite + TypeScript.

## Backend

### Requisitos
- Python 3.11+

### Instalación
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
pip install -r requirements.txt
cp .env.example .env
```

### Ejecutar
```bash
uvicorn main:app --reload
```

### Endpoint base
- Health: `GET /api/health`

## Frontend

### Requisitos
- Node.js 20+

### Instalación
```bash
cd frontend
npm install
```

### Ejecutar
```bash
npm run dev
```

## Notas
- Arquitectura monolítica modular por dominios.
- Módulos de WhatsApp, notificaciones, scheduler y PDF están creados con lógica mínima base.


### Tests
```bash
pip install -r backend/requirements.txt
pytest -q backend/tests
```
