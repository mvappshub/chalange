# Deploy (rychle)

## Varianta A: Render / Fly / Railway
- Build: Dockerfile
- Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

## Varianta B: VPS
```bash
docker compose up --build -d
```

## Zálohy
- mountni volume `./backups` a pravidelně spouštěj `python scripts/backup.py` (cron/GitHub Action/CI job)
