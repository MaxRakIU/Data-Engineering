# Data Dictionary (Template)

## Tabelle: facts (curated)
- `timestamp` (STRING/ISO8601): Zeitstempel
- `value` (NUMBER): Beispielwert
- Herkunft: Pipeline-Schritt `transform`
- Partitionierung: nach Ausführungsdatum (im Beispiel über Verzeichnisstruktur)

## Rohdaten
- CSV mit Spalten `timestamp`, `value`
- Quelle: Demo-Generator (`ingest.py`)
