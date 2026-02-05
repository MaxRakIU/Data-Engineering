# Lakehouse (Batch) – Lokaler Mikroservice-Stack

Dieses Repo bietet ein **lokales, reproduzierbares Lakehouse** fuer Batch-Verarbeitung mit:
- **MinIO** (S3-compatible object storage)
- **Apache Spark** (Batch-Verarbeitung)
- **Apache Iceberg** (ACID tables)
- **Great Expectations** (Datenqualitaet + Quarantaene)
- **Apache Airflow** (Orchestrierung: extract → validate → transform → publish)
- **Trino** (optionale Query-Engine)

## Schnellstart
1) `.env` aus `.env.example` erstellen und bei Bedarf anpassen.
2) Stack starten:

```bash
make up
```

3) Services pruefen:

```bash
make ps
```

## Ports & Zugangsdaten
- **Airflow**: http://localhost:8082 (User `admin`, Passwort `admin`)
- **MinIO**: http://localhost:9101 (Konsole), http://localhost:9100 (S3 API)
- **Spark UI**: http://localhost:8181
- **Trino**: http://localhost:8085

## Repository-Struktur
- `airflow/` – DAGs, Plugins, Logs
- `data/` – raw, staging, curated, quarantine
- `docker/` – Service-Konfigurationen
- `docs/` – Architektur-Notizen und Entscheidungen
- `great_expectations/` – GE-Konfiguration, Checkpoints, Erwartungen
- `jobs/` – Spark Batch-Jobs
- `scripts/` – Helfer-Skripte (Bootstrap, Submit)
- `trino/` – Trino-Konfigurationen/Kataloge

## Doku-Links
- `docs/architecture.md` – Architektur-Notizen
- `docs/diagram.txt` – ASCII-Uebersicht
- `docs/runbook.md` – Start/Stop/Checks
- `docs/github_upload.md` – GitHub-Upload-Checkliste

## Pipeline-Stufen
- **extract**: offene Daten nach `raw/` laden
- **validate**: GE-Checks; fehlerhafte Batches nach `quarantine/`
- **transform**: Bereinigung nach `staging/` (Parquet)
- **publish**: Schreiben von `curated/` als Iceberg-Tabellen

## Datensatz-Auswahl (Open Data)
Der DAG kann mit jeder CSV laufen. Uebergabe ueber DAG-Parameter:

```bash
docker compose exec -T airflow \
  airflow dags trigger lakehouse_batch_pipeline \
  -c '{"RAW_S3_KEY":"big_ok.csv","LOCAL_FILE_PATH":"/opt/data/source/big_ok.csv","SKIP_IF_EXISTS":"false"}'
```

Hinweise:
- `RAW_S3_KEY` definiert den MinIO-Key unter `raw/`.
- `LOCAL_FILE_PATH` zeigt auf die Datei im Airflow-Container (`/opt/data/...` kommt aus `data/`).
- `SKIP_IF_EXISTS` erlaubt Re-Runs ohne Raw zu ueberschreiben.

## Hinweise zu Spark-Jobs
- Transform/Publish laufen in `local[*]`, um lokale Worker-Probleme zu vermeiden.

## Smoke-Check
Nach dem Lauf die Outputs pruefen:

```bash
make smoke
```

## Demo-Run (ein Befehl)
Startet Services und triggert den DAG mit `big_ok.csv`:

```bash
make demo
```

## Abgabe-Checks
Fuehrt Smoke-Check + Trino-Zaehler aus:

```bash
make precheck
```

## Packaging fuer Abgabe
Erstellt `lakehouse-new-submission.tar.gz` ohne Logs/DB/Data:

```bash
make package
```

## Daten-Governance & Datenschutz
- Optionales Masking in `transform_to_staging.py`:
  - `SENSITIVE_COLUMNS=email,phone`
  - `MASK_STRATEGY=hash` (or `redact`)
- Qualitaets-Reports werden nach `quality/reports/...` geschrieben.

## Zugriffskontrolle
- **Trino** laeuft im Read-only-Modus (Write-Queries sind blockiert).
- **MinIO** optionaler Read-only-User ueber:
  - `MINIO_READONLY_USER`, `MINIO_READONLY_PASSWORD`

## Zuverlaessigkeit / Skalierbarkeit / Wartbarkeit
- **Zuverlaessigkeit**: GE-Validierung + Quarantaene; Iceberg ACID-Writes.
- **Skalierbarkeit**: Parquet-Speicher, Trennung von Speicher/Compute (MinIO + Spark).
- **Wartbarkeit**: containerisierte Services, Makefile-Workflows, klare Ordnerstruktur.
