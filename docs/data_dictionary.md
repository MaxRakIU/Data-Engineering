###Data Dictionary (docs/data_dictionary.md -- kompletter Inhalt)\
\# Data Dictionary\
\
\## Rohdaten (data/raw/\<YYYY-MM-DD\>/data.csv)\
- timestamp: ISO-Zeitstempel im Minutenraster (DWD 10-Minuten-Raster).\
- value: Lufttemperatur in °C (numerisch).\
\
Quelle: Deutscher Wetterdienst (DWD), Climate Data Center, Beobachtungen
Deutschland, 10-Minuten, Lufttemperatur (Teil „recent").\
Fehlwerte werden beim Merge gefiltert (spezielle DWD-Codes) und in der
Validierung verworfen.\
\
\## Staging (data/staging/\<YYYY-MM-DD\>/agg.csv)\
- day: Datum (YYYY-MM-DD).\
- count: Anzahl gültiger Messwerte am Tag.\
- min: Tagesminimum (°C).\
- max: Tagesmaximum (°C).\
- mean: Tagesmittel (°C).\
\
\## Curated (data/curated/\<YYYY-MM-DD\>/facts.csv)\
Identisch zu Staging; als freigegebene Zieltabelle für Auswertungen.\
\
\
