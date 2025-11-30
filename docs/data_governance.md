\# Data Governance\
\
Herkunft & Lizenz\
Offene Messdaten des DWD (Lufttemperatur, 10-Minuten). Nutzung gemäß
Open-Data-Bedingungen.\
\
Zonen & Zugriff\
Trennung in raw, staging, curated, quarantine.\
Lokaler Zugriff für Projektzwecke; in realen Umgebungen rollenbasierte
Rechte.\
\
Qualitätssicherung (Quality Gate)\
Pflichtspalten (timestamp, value), Mindestzeilen je Batch,
Plausibilitätsbereich −50...+50 °C.\
Bei Verstößen: kompletter Batch → \*quarantine\* (keine
Weiterverarbeitung).\
Fehlerursache im Log dokumentiert.\
\
Versionierung & Reproduzierbarkeit\
Containerisierte Ausführung (docker-compose), datumsbasierte Batch-Runs,
Codeversionierung im Git-Repository, „How-to-run" im README.\
\
Aufbewahrung\
Rohdaten längerfristig; curated gemäß Nutzungsbedarf; Quarantäne nur zur
Fehleranalyse, danach Bereinigung.
