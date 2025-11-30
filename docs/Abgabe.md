{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 Umsetzungsnotiz (Phase 2)\
\
Die in Phase 1 konzipierte Batch-Pipeline wurde lokal containerisiert implementiert und reproduzierbar ausgef\'fchrt. Verarbeitet wird ein offener DWD-Datensatz (10-Minuten-Lufttemperatur, Teil \'84recent\'93). Der Batch-Ablauf umfasst vier Schritte: \
1. Extraktion: legt den Tages-Batch im Rohbereich ab\
\
2. Validierung: erzwingt Pflichtspalten (timestamp,value), Mindestzeilen und einen Plausibilit\'e4tsbereich (\uc0\u8722 50\'85+50 \'b0C) und verschiebt fehlerhafte Batches konsequent in eine Quarant\'e4ne\
\
3. Transformation: f\'fchrt eine speicherschonende Online-Aggregation je Tag durch (count, min, max, mean)\
\
4. Ver\'f6ffentlichung: stellt die Tageskennzahlen im Bereich *curated* bereit. Die Umsetzung trennt Datenzonen (raw, staging, curated, quarantine), ist robust gegen\'fcber fehlerhaften Eingaben. \
\
Reproduzierbarkeit wird durch docker-compose und eine kurze \'84How-to-run\'93-Anleitung im Repository sichergestellt. \
\
Als Evidenz werden der DAG-Graph, ein Dateibaum der erzeugten Verzeichnisse und die Ausgabedateien bereitgestellt. \
Die L\'f6sung adressiert Zuverl\'e4ssigkeit (Quality-Gate, Quarant\'e4ne), Skalierbarkeit (Batch-Verarbeitung, speicherschonende Aggregation auf 36 M Zeilen) und Wartbarkeit (klare Struktur, getrennte Skripte). \
Ein sp\'e4terer Wechsel auf spaltenorientierte Formate bzw. andere Compute-Engines ist ohne Strukturbruch m\'f6glich.\
}