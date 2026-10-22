#!/usr/bin/env python3
"""phy_replay_2024.py - repeat, on this machine, the replay that tested gate edition 2026-10-21 in the project chat.

It copies the vault to /home/claude/replay-2024 (without vault/work), removes the 2024 year check's fixes
(ER-B06-013 to ER-B06-027) from the copy's ERRATA, so 2024's rows read as they did before that check, and compares
2024's own check files (outputs/logs/doublecheck/B06) with the copy both ways, then runs the lint over 2024.
Nothing outside /home/claude/replay-2024 is touched: no vault file, no report, no log, no git.

  python3 /mnt/project/phy_replay_2024.py

Expected output (PHY-08 Y§0.5 step 3; PHY-AUDIT-2024-B06):
  errata removed 15 | YC-2024 raw 132 | YC-2024 normalised 62 | YC-2024-2024-5531 raw 29 |
  YC-2024-2024-5531 normalised 5 | LINT 2024 | 6 finding(s): figure-measured 6
Anything else: use `phy_gate.py yearcheck ... --compare --raw` in the year checks and say so in one line.
Paths can be changed with RP_VAULT, RP_CHECKS, RP_GATE, RP_ENV and RP_DIR (used only to test this script).
"""
import csv, json, os, shutil, subprocess
V = os.environ.get("RP_VAULT", "/home/claude/vault")
CHECKS = os.environ.get("RP_CHECKS", "/mnt/user-data/outputs/logs/doublecheck/B06")
GATE = os.environ.get("RP_GATE", "/home/claude/phy_gate.py")
ENV0 = os.environ.get("RP_ENV", "/home/claude/phy_env.json")
R = os.environ.get("RP_DIR", "/home/claude/replay-2024")
shutil.rmtree(R, ignore_errors=True)
shutil.copytree(V, R + "/vault", ignore=shutil.ignore_patterns("work"))
for d in ("vault/work", "home", "reports", "logs"):
    os.makedirs(os.path.join(R, d), exist_ok=True)
for f in os.listdir(CHECKS):
    if f.startswith("YC-2024") and f.endswith(".csv"):
        shutil.copy2(os.path.join(CHECKS, f), R + "/vault/work/")
p = R + "/vault/l1/ERRATA.csv"                      # the vault as it stood before the year check's fixes
rows = list(csv.DictReader(open(p, encoding="utf-8")))
keep = [r for r in rows if not ("ER-B06-013" <= r["errata_id"] <= "ER-B06-027")]
with open(p, "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    w.writerows(keep)
E = json.load(open(ENV0))
E.update(vault=R + "/vault", home=R + "/home", reports_dir=R + "/reports", logs_dir=R + "/logs")
json.dump(E, open(R + "/phy_env.json", "w"))
env = dict(os.environ, PHY_ENV=R + "/phy_env.json")
out = [f"errata removed {len(rows) - len(keep)}"]
for paper, unit in (("", "YC-2024"), ("2024-5531", "YC-2024-2024-5531")):
    for raw in (True, False):
        cmd = ["python3", GATE, "yearcheck", "2024"] + (["--paper", paper] if paper else []) + ["--compare"] + (["--raw"] if raw else [])
        subprocess.run(cmd, env=env, capture_output=True, text=True)
        n = sum(1 for _ in csv.DictReader(open(f"{R}/vault/work/{unit}__DIFF.csv", encoding="utf-8")))
        out.append(f"{unit} {'raw' if raw else 'normalised'} {n}")
lint = subprocess.run(["python3", GATE, "lint", "--all", "--year", "2024"], env=env, capture_output=True, text=True).stdout.splitlines()
print(" | ".join(out) + " | " + (lint[0].split(" ->")[0] if lint else "lint: no output"))
