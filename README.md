
# Data-Engineering
=======
# Balanced Lakehouse – Grundgerüst (lokal)

Dieses Grundgerüst startet Airflow (Webserver + Scheduler), Postgres und MinIO.
Die Beispiel-DAG `batch_lakehouse_daily` demonstriert einen einfachen Batch-Flow mit lokalen Dateien.

## Voraussetzungen
- Docker & Docker Compose
- (Optional) `make`

## Start
```bash
make init      # einmalig: Airflow DB initialisieren und Admin-User anlegen
make up        # Services starten
make web       # URL und Logins ausgeben
```

Airflow UI: http://localhost:8080  (User: admin / Pass: admin)

## Beispiel-DAG ausführen
```bash
make trigger   # DAG "batch_lakehouse_daily" starten
```

## Was passiert im Beispiel?
- **extract**: erzeugt Demo-Daten als CSV unter `./data/raw/<Ausführungsdatum>/data.csv`.
- **validate**: prüft, ob die Datei existiert und mehr als eine Zeile hat.
- **transform**: erzeugt eine "Aggregation" (hier: einfache Kopie mit Datumsstempel) nach `./data/staging/<Ausführungsdatum>/agg.csv`.
- **publish**: kopiert die Datei nach `./data/curated/<Ausführungsdatum>/facts.csv`.

> Hinweis: Dieses Minimalbeispiel nutzt lokale Dateien, um den Ablauf zu demonstrieren.
> Die Umstellung auf MinIO/S3-Pfade kann später schrittweise erfolgen (z. B. per AWS/MinIO-Client oder Airflow-Operatoren).

## Ordnerstruktur
```
dags/                 # Airflow DAGs
jobs/                 # Skripte für Tasks (ohne externe Abhängigkeiten)
data/{raw,staging,curated,quarantine}/
docs/                 # Doku-Templates (Data Dictionary, Governance)
```

## Beenden
```bash
make down
```

## Ergebnis (Phase 2)
End-to-End-Run erfolgreich (36 Mio. Zeilen möglich, speicherschonende Aggregation je Tag).
Quality-Gate belegt: mehrere grüne Runs (curated), 1 absichtlich fehlerhafter Run (quarantine).
Evidenz: `docs/graph.png`, `docs/data_tree.txt`, Logauszüge in Airflow-UI.
