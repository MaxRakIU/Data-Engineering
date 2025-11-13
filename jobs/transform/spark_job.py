import argparse, os, csv, datetime

parser = argparse.ArgumentParser()
parser.add_argument("--inp", required=True, help="Input CSV path")
parser.add_argument("--out", required=True, help="Output CSV path")
args = parser.parse_args()

os.makedirs(os.path.dirname(args.out), exist_ok=True)

# demo "aggregation": copy and append a note column with execution date
exec_date = datetime.date.today().isoformat()

with open(args.inp, "r") as fin, open(args.out, "w", newline="") as fout:
    r = csv.reader(fin)
    w = csv.writer(fout)
    header = next(r)
    w.writerow(header + ["note"])
    for row in r:
        w.writerow(row + [f"aggregated:{exec_date}"])

print(f"Wrote demo aggregate to {args.out}")
