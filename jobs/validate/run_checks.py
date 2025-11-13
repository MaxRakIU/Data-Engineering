import argparse, os, sys, shutil

parser = argparse.ArgumentParser()
parser.add_argument("--inp", required=True, help="Input CSV path")
parser.add_argument("--quarantine", required=True, help="Quarantine dir if fails")
args = parser.parse_args()

# Simple checks: file exists and has more than one line
if not os.path.exists(args.inp):
    print(f"[ERROR] Missing file: {args.inp}")
    os.makedirs(args.quarantine, exist_ok=True)
    sys.exit(1)

with open(args.inp, "r") as f:
    lines = f.readlines()

if len(lines) <= 1:
    print(f"[ERROR] Not enough data lines in {args.inp}")
    os.makedirs(args.quarantine, exist_ok=True)
    shutil.move(args.inp, os.path.join(args.quarantine, os.path.basename(args.inp)))
    sys.exit(1)

print("[OK] Basic checks passed.")
