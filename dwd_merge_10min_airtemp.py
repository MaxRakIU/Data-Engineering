#!/usr/bin/env python3
import zipfile, os, csv, re, datetime

SRC_DIR = "data/source/dwd_10min_airtemp/recent"    # hier liegen die heruntergeladenen ZIPs
OUT_CSV = "data/source/big.csv"

os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)

def parse_ts(s):
    # DWD 10-Minuten hat oft MESS_DATUM oder MESS_DATUM_WOZ: z.B. 20250101 00:10 oder 202501010010
    s = re.sub(r"\D", "", s)  # nur Ziffern
    if len(s) == 12:  # YYYYMMDDhhmm
        dt = datetime.datetime.strptime(s, "%Y%m%d%H%M")
    elif len(s) == 8:  # YYYYMMDD (fallback)
        dt = datetime.datetime.strptime(s, "%Y%m%d")
    else:
        return None
    return dt.isoformat(timespec="minutes")

def find_temp_col(header):
    # Suche eine Temperaturspalte (beim 10-Min-Produkt beginnt oft mit 'TT')
    hl = [h.strip().lower() for h in header]
    for i, h in enumerate(hl):
        if h.startswith("tt"):   # TT_10 / TT_TU etc.
            return i
    return None

rows_out = []
for root, _, files in os.walk(SRC_DIR):
    for fn in files:
        if not fn.lower().endswith(".zip"):
            continue
        path = os.path.join(root, fn)
        with zipfile.ZipFile(path) as zf:
            for name in zf.namelist():
                if not name.lower().endswith(".txt"):
                    continue
                with zf.open(name) as f:
                    # Dateien sind ;-getrennt, mit Kopfzeilen und Kommentaren (#)
                    text = f.read().decode("utf-8", errors="ignore").splitlines()
                    # Kommentare entfernen
                    data = [ln for ln in text if not ln.startswith("#") and ln.strip()]
                    if not data:
                        continue
                    reader = csv.reader(data, delimiter=';')
                    header = next(reader, None)
                    if not header:
                        continue
                    # Zeitspalte finden
                    header_l = [h.strip().lower() for h in header]
                    ts_idx = None
                    for cand in ("mess_datum_woz", "mess_datum"):  # beide vorkommend
                        if cand in header_l:
                            ts_idx = header_l.index(cand)
                            break
                    val_idx = find_temp_col(header)
                    if ts_idx is None or val_idx is None:
                        continue
                    for row in reader:
                        if len(row) <= max(ts_idx, val_idx):
                            continue
                        ts = parse_ts(row[ts_idx])
                        if not ts:
                            continue
                        v = row[val_idx].strip().replace(",", ".")  # Dezimal-Komma
                        if v in ("", "-999", "-999.0"):  # DWD-Fehlwerte aussortieren
                            continue
                        try:
                            float(v)
                        except:
                            continue
                        rows_out.append((ts, v))

# Sortieren und schreiben
rows_out.sort(key=lambda x: x[0])
os.makedirs(os.path.dirname(OUT_CSV), exist_ok=True)
with open(OUT_CSV, "w", newline="") as fout:
    w = csv.writer(fout)
    w.writerow(["timestamp", "value"])
    w.writerows(rows_out)

print(f"geschrieben: {OUT_CSV} mit {len(rows_out):,} Zeilen")
