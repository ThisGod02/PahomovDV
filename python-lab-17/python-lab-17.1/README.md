# Lab 17.1 - Deploy Pack

This folder reuses the existing practical apps from previous labs:

- `frontend/` - Next.js portfolio site
- `backend/` - FastAPI book API

Added on top:
- containerization files for the backend
- Vercel deployment helper config for the frontend
- local smoke test

Useful commands:

```bash
cd backend
python -m pytest test_smoke.py -q

cd ../frontend
npm run build
```

Backend Docker build:

```bash
cd backend
docker build -t lab17-book-api .
docker run -p 8000:8000 lab17-book-api
```
