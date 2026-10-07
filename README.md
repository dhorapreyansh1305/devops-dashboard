# DevOps Dashboard

Runnable full-stack starter using React + TypeScript + Vite, FastAPI, PostgreSQL, Docker Compose, and Nginx.

## Features
- JWT login
- Dashboard overview
- Server inventory
- Docker container inventory when Docker socket is mounted
- Deployment records
- Pipeline records
- Metrics endpoint
- Health check
- PostgreSQL persistence
- Nginx reverse proxy
- Seeded demo data

## Run

```bash
cp .env.example .env
docker compose up --build
```

Open http://localhost

Demo login:
- Email: `admin@example.com`
- Password: `admin123`

API docs: http://localhost/docs

## Development

Backend:
```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Frontend:
```bash
cd frontend
npm install
npm run dev
```

For production, replace demo credentials/secrets, restrict CORS, use HTTPS, and do not expose the Docker socket without a deliberate security design.
