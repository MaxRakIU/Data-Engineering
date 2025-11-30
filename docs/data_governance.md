{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 # Data Governance\
\
Herkunft & Lizenz\
Offene Messdaten des DWD (Lufttemperatur, 10-Minuten). Nutzung gem\'e4\'df Open-Data-Bedingungen.\
\
Zonen & Zugriff \
Trennung in raw, staging, curated, quarantine. \
Lokaler Zugriff f\'fcr Projektzwecke; in realen Umgebungen rollenbasierte Rechte.\
\
Qualit\'e4tssicherung (Quality Gate)\
Pflichtspalten (timestamp, value), Mindestzeilen je Batch, Plausibilit\'e4tsbereich \uc0\u8722 50\'85+50 \'b0C. \
Bei Verst\'f6\'dfen: kompletter Batch \uc0\u8594  *quarantine* (keine Weiterverarbeitung). \
Fehlerursache im Log dokumentiert.\
\
Versionierung & Reproduzierbarkeit\
Containerisierte Ausf\'fchrung (docker-compose), datumsbasierte Batch-Runs, Codeversionierung im Git-Repository, \'84How-to-run\'93 im README.\
\
Aufbewahrung\
Rohdaten l\'e4ngerfristig; curated gem\'e4\'df Nutzungsbedarf; Quarant\'e4ne nur zur Fehleranalyse, danach Bereinigung.\
}