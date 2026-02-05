# Architektur-Notizen

## Mikroservices
- MinIO (Objektspeicher)
- Spark Master/Worker (Batch-Compute)
- Airflow (Orchestrierung)
- Trino (Query-Layer)

## Datenfluss
extract → validate → transform → publish

## Speicher
- Raw/Staging/Curated liegen in MinIO (S3-kompatibel)
- Spark liest/schreibt ueber `s3a://` Pfade

## Zuverlaessigkeit
- Airflow Retries + Logs
- GE-Qualitaetschecks und Quarantaene
- Iceberg ACID-Tabellen

## Skalierbarkeit
- Parquet spaltenorientiert
- Partitionierung (in Transform erweiterbar)
- Speicher/Compute getrennt

## Wartbarkeit
- Containerisierte Services
- Klare Ordnerstruktur
- Makefile fuer reproduzierbaren Start

## Datensicherheit & Governance
- S3-Zugriff ueber Credentials
- Quarantaene fuer ungueltige Batches
- Versionierte Iceberg-Tabellen
