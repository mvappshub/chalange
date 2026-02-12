# Release proces (mini)

## Verze
- Použij semver: `MAJOR.MINOR.PATCH`
- V PR používej Conventional Commits (např. `feat: ...`, `fix: ...`), aby šel changelog generovat.

## Checklist
1) `ruff check .` + `PYTHONPATH=. pytest`
2) Aktualizuj `CHANGELOG.md`
3) Bump verze v `app/main.py` (a případně v pyproject)
4) Tagni release:
```bash
git tag v0.1.0
git push --tags
```

## Docker image
- Lokálně:
```bash
docker build -t opsboard:0.1.0 .
docker run -p 8000:8000 opsboard:0.1.0
```

## Nasazení
- Platformy typu Render/Fly/Railway: použij Dockerfile (viz `DEPLOYMENT.md`)
