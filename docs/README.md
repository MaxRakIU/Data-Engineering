{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
{\*\listtable{\list\listtemplateid1\listhybrid{\listlevel\levelnfc23\levelnfcn23\leveljc0\leveljcn0\levelfollow0\levelstartat1\levelspace360\levelindent0{\*\levelmarker \{disc\}}{\leveltext\leveltemplateid1\'01\uc0\u8226 ;}{\levelnumbers;}\fi-360\li720\lin720 }{\listname ;}\listid1}
{\list\listtemplateid2\listhybrid{\listlevel\levelnfc23\levelnfcn23\leveljc0\leveljcn0\levelfollow0\levelstartat1\levelspace360\levelindent0{\*\levelmarker \{disc\}}{\leveltext\leveltemplateid101\'01\uc0\u8226 ;}{\levelnumbers;}\fi-360\li720\lin720 }{\listname ;}\listid2}}
{\*\listoverridetable{\listoverride\listid1\listoverridecount0\ls1}{\listoverride\listid2\listoverridecount0\ls2}}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 ## How to run (local)\
\
docker compose up airflow-init\
docker compose up -d\
# UI: http://localhost:8080  (admin/admin)\
docker compose exec airflow-webserver airflow dags trigger batch_lakehouse_daily\
\pard\tx220\tx720\pardeftab720\li720\fi-720\sa240\partightenfactor0
\ls1\ilvl0
\fs26 \cf0 \expnd0\expndtw0\kerning0
\
\pard\tx220\tx720\pardeftab720\li720\fi-720\sa240\partightenfactor0
\cf0 ## Ergebnis (Phase 2)\
End-to-End-Run erfolgreich (36 Mio. Zeilen m\'f6glich, speicherschonende Aggregation je Tag).\
Quality-Gate belegt: mehrere gr\'fcne Runs (curated), 1 absichtlich fehlerhafter Run (quarantine).\
Evidenz: `docs/graph.png`, `docs/data_tree.txt`, Logausz\'fcge in Airflow-UI.\
\pard\tx220\tx720\pardeftab720\li720\fi-720\sa240\partightenfactor0
\ls2\ilvl0\cf0 \
\pard\tx220\tx720\pardeftab720\li720\fi-720\sa240\partightenfactor0
\ls2\ilvl0
\fs24 \cf0 \
}