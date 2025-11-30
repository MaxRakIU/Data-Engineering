{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;\red0\green0\blue0;}
{\*\expandedcolortbl;;\cssrgb\c0\c0\c0;}
{\*\listtable{\list\listtemplateid1\listhybrid{\listlevel\levelnfc23\levelnfcn23\leveljc0\leveljcn0\levelfollow0\levelstartat1\levelspace360\levelindent0{\*\levelmarker \{disc\}}{\leveltext\leveltemplateid1\'01\uc0\u8226 ;}{\levelnumbers;}\fi-360\li720\lin720 }{\listname ;}\listid1}}
{\*\listoverridetable{\listoverride\listid1\listoverridecount0\ls1}}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 ###Data Dictionary (docs/data_dictionary.md \'96 kompletter Inhalt)\
# Data Dictionary\
\
## Rohdaten (data/raw/<YYYY-MM-DD>/data.csv)\
- timestamp: ISO-Zeitstempel im Minutenraster (DWD 10-Minuten-Raster).\
- value: Lufttemperatur in \'b0C (numerisch).\
\
Quelle: Deutscher Wetterdienst (DWD), Climate Data Center, Beobachtungen Deutschland, 10-Minuten, Lufttemperatur (Teil \'84recent\'93). \
Fehlwerte werden beim Merge gefiltert (spezielle DWD-Codes) und in der Validierung verworfen.\
\
## Staging (data/staging/<YYYY-MM-DD>/agg.csv)\
- day: Datum (YYYY-MM-DD).  \
- count: Anzahl g\'fcltiger Messwerte am Tag.  \
- min: Tagesminimum (\'b0C).  \
- max: Tagesmaximum (\'b0C).  \
- mean: Tagesmittel (\'b0C).\
\
## Curated (data/curated/<YYYY-MM-DD>/facts.csv)\
Identisch zu Staging; als freigegebene Zieltabelle f\'fcr Auswertungen.\
\pard\tx220\tx720\pardeftab720\li720\fi-720\sa240\partightenfactor0
\ls1\ilvl0
\fs26 \cf0 \expnd0\expndtw0\kerning0
\outl0\strokewidth0 \strokec2 \
\
\pard\tx220\tx720\pardeftab720\li720\fi-720\sa240\partightenfactor0
\ls1\ilvl0
\fs24 \cf0 \
}