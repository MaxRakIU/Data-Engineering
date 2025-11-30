import argparse, os, shutil

parser = argparse.ArgumentParser()
parser.add_argument("--src", required=False, default="data/source/big.csv", help="Input CSV on host (mounted)")
parser.add_argument("--out", required=True, help="Output CSV path (inside container mount)")
args = parser.parse_args()

# Container sieht ./data als /opt/airflow/data; die relativen Pfade funktionieren 1:1
os.makedirs(os.path.dirname(args.out), exist_ok=True)

assert os.path.exists(args.src), f"Quelle fehlt: {args.src}"
shutil.copyfile(args.src, args.out)
print(f"[INGEST] copied {args.src} -> {args.out}")
