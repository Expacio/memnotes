
# Memnotes - Separated Backend & Frontend (Generated)

This repo contains a separated architecture for your Memnotes app:

- `backend/` - Flask API-only backend (app.py). Uses sqlite by default (users.db).
- `frontend/` - Next.js frontend skeleton (pages based). Configure `NEXT_PUBLIC_API_URL` to point to your backend.

## Quick local run (dev)

### Backend
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

Set `NEXT_PUBLIC_API_URL` in `.env.local` or in your Vercel environment variables to `http://localhost:5000` (or production URL).

## Deploying
- Push this repo to GitHub.
- On Vercel: import the GitHub repo. Set `NEXT_PUBLIC_API_URL` to your backend URL.
- For the backend, deploy to Render, Fly, Railway, or a VPS. Alternatively, convert backend to a serverless function later.

## Notes
- I kept the original `search.py` logic in `backend/search.py` so you can re-enable advanced searching.
- The frontend uses a simple `username=demo` pattern for quick testing. Replace with session-based auth once you host backend with proper cookies/CORS credentials enabled.
