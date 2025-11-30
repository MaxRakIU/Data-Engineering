import argparse, os, sys, csv, shutil

# --- Parameter (bei Bedarf anpassen) ---
MIN_ROWS = 1000                     # Mindestzeilen je Batch
REQUIRED = {"timestamp", "value"}   # Pflichtspalten
MIN_VALUE = -50.0                   # plausibler Bereich (DWD Lufttemp in °C)
MAX_VALUE =  50.0

parser = argparse.ArgumentParser()
parser.add_argument("--inp", required=True, help="Input CSV path")
parser.add_argument("--quarantine", required=True, help="Quarantine dir if fails")
args = parser.parse_args()

def fail(msg):
    print(f"[ERROR] {msg}")
    os.makedirs(args.quarantine, exist_ok=True)
    if os.path.exists(args.inp):
        shutil.move(args.inp, os.path.join(args.quarantine, os.path.basename(args.inp)))
        print(f"[INFO] moved to quarantine: {args.quarantine}")
    sys.exit(1)

if not os.path.exists(args.inp):
    fail(f"Missing file: {args.inp}")

with open(args.inp, "r") as f:
    r = csv.reader(f)
    header = next(r, None)
    if not header:
        fail("Empty file (no header)")
    header_l = [h.strip().lower() for h in header]
    if not REQUIRED.issubset(set(header_l)):
        fail(f"Missing required columns {REQUIRED} in header {header}")
    ti = header_l.index("timestamp")
    vi = header_l.index("value")

    rows = 0
    bad = 0
    for row in r:
        rows += 1
        if len(row) <= max(ti, vi):
            bad += 1; continue
        v_str = row[vi].strip().replace(",", ".")  # deutsches Dezimal-Komma erlauben
        try:
            v = float(v_str)
        except:
            bad += 1; continue
        if not (MIN_VALUE <= v <= MAX_VALUE):
            bad += 1

if rows < MIN_ROWS:
    fail(f"Too few data rows: {rows} < {MIN_ROWS}")
if bad > 0:
    fail(f"{bad} invalid rows (type/range)")

print(f"[OK] Validation passed: rows={rows}, bad=0, range=[{MIN_VALUE},{MAX_VALUE}]")
