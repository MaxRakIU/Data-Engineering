# Runbook (Kurz)

## Start
```bash
make up
```

## Demo-Run (CSV)
```bash
make demo
```

## Status/Logs
```bash
make ps
make logs
```

## Abgabe-Checks
```bash
make precheck
```

## Stoppen
```bash
make down
```

## Haeufige Probleme
- **Airflow UI nicht erreichbar**: Container neu starten: `docker compose up -d --force-recreate airflow`
- **Spark haengt auf Worker**: Transform/Publish laufen in `local[*]` (siehe DAG)
- **Trino startet nicht**: Logs pruefen: `docker compose logs trino`
