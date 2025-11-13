import argparse, os, csv, datetime

parser = argparse.ArgumentParser()
parser.add_argument("--out", required=True, help="Output CSV path")
args = parser.parse_args()

out_path = args.out
os.makedirs(os.path.dirname(out_path), exist_ok=True)

today = datetime.date.today()
rows = [
    ["timestamp", "value"],
    [f"{today}T00:00:00", "10"],
    [f"{today}T01:00:00", "12"],
    [f"{today}T02:00:00", "11"],
]

with open(out_path, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(rows)

print(f"Wrote demo data to {out_path}")
