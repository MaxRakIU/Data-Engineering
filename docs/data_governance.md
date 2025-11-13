# Data Governance (Kurzleitfaden)

- **Herkunft:** Offene Quelle (im Demo: Generator). Dokumentation im Repository.
- **Zugriff:** Schreib-/Leserechte getrennt (Roh, Staging, Curated). Im Demo: Dateisystemordner.
- **Qualität:** Mindestprüfungen (Existenz, Zeilenzahl). Erweiterbar um inhaltliche Regeln.
- **Versionierung:** Runs pro Ausführungsdatum im Pfad; Erweiterbar um Tabellenversionen.
- **Aufbewahrung:** Rohdaten länger, Curated gemäß Bedarf; definiert in Projektleitfaden.
- **Sicherheit:** In Produktion: Verschlüsselung at-rest/in-transit, Zugriff per Rollen.
