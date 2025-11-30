Umsetzungsnotiz (Phase 2)\
\
Die in Phase 1 konzipierte Batch-Pipeline wurde lokal containerisiert
implementiert und reproduzierbar ausgeführt. Verarbeitet wird ein
offener DWD-Datensatz (10-Minuten-Lufttemperatur, Teil „recent"). Der
Batch-Ablauf umfasst vier Schritte:\
1. Extraktion: legt den Tages-Batch im Rohbereich ab\
\
2. Validierung: erzwingt Pflichtspalten (timestamp,value), Mindestzeilen
und einen Plausibilitätsbereich (−50...+50 °C) und verschiebt
fehlerhafte Batches konsequent in eine Quarantäne\
\
3. Transformation: führt eine speicherschonende Online-Aggregation je
Tag durch (count, min, max, mean)\
\
4. Veröffentlichung: stellt die Tageskennzahlen im Bereich \*curated\*
bereit. Die Umsetzung trennt Datenzonen (raw, staging, curated,
quarantine), ist robust gegenüber fehlerhaften Eingaben.\
\
Reproduzierbarkeit wird durch docker-compose und eine kurze
„How-to-run"-Anleitung im Repository sichergestellt.\
\
Als Evidenz werden der DAG-Graph, ein Dateibaum der erzeugten
Verzeichnisse und die Ausgabedateien bereitgestellt.\
Die Lösung adressiert Zuverlässigkeit (Quality-Gate, Quarantäne),
Skalierbarkeit (Batch-Verarbeitung, speicherschonende Aggregation auf 36
M Zeilen) und Wartbarkeit (klare Struktur, getrennte Skripte).\
Ein späterer Wechsel auf spaltenorientierte Formate bzw. andere
Compute-Engines ist ohne Strukturbruch möglich.
