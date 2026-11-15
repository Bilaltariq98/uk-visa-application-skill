#!/usr/bin/env python3
"""GO / NO-GO check before submitting a UK visa application.

Lives in <workspace>/submit/ next to case.json. Run from anywhere:
  python3 submit/preflight.py                     exit 0 = GO, 1 = NO-GO
  python3 submit/preflight.py --today 2027-01-05  simulate another date
  python3 submit/preflight.py --selftest

All case-specific values live in case.json (see assets/case.example.json).
Filenames carry dates (YYYY-MM-DD) so freshness can be computed.
"""
import json
import re
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def d(s):
    return date.fromisoformat(s)


def last_months(day, n):
    """[(y, m)] for the n calendar months ending with day's month, oldest first."""
    y, m, out = day.year, day.month, []
    for _ in range(n):
        out.append((y, m))
        y, m = (y, m - 1) if m > 1 else (y - 1, 12)
    return out[::-1]


def files(folder):
    p = ROOT / folder
    return sorted(f for f in p.iterdir() if f.is_file() and not f.name.startswith(".")) if p.is_dir() else []


def dated(folder, pattern):
    """[(date, path)] for files whose name matches pattern; uses group 'end' if present, else 'date'."""
    rx, out = re.compile(pattern, re.I), []
    for f in files(folder):
        if m := rx.search(f.name):
            g = m.groupdict()
            out.append((d(g.get("end") or g["date"]), f))
    return out


def check_fresh(today, label, found, max_age):
    if not found:
        return [f"{label}: no matching file found."]
    newest = max(dt for dt, _ in found)
    age = (today - newest).days
    if age > max_age:
        return [f"{label}: newest is dated {newest} ({age} days old, max {max_age}). Get a newer one."]
    return []


def check_series(label, paydays, ranges, months):
    """paydays [date], ranges [(start, end)] -> (blockers, window). Consecutive months ending at the latest payday."""
    if not paydays:
        return [f"{label}: none found."], []
    by_month = {(p.year, p.month): p for p in paydays}
    window = last_months(max(paydays), months)
    out = []
    for ym in window:
        p = by_month.get(ym)
        if not p:
            out.append(f"{label}: missing {ym[0]}-{ym[1]:02d}.")
        elif ranges is not None and not any(s <= p <= e for s, e in ranges):
            out.append(f"{label}: no statement covers {p}.")
    return out, window


def placeholder_lines(rel, markers):
    p = ROOT / rel
    if not p.exists():
        return [f"{rel} is missing."]
    return [f"{rel}:{i}: {ln.strip()[:120]}" for i, ln in enumerate(p.read_text().splitlines(), 1) if any(m in ln for m in markers)]


def main(today, case):
    blockers, warnings, uploads = [], [], []
    expires = d(case["leave_expires"])
    left = (expires - today).days
    if left <= 0:
        print(f"NO-GO. Current permission expired on {expires}. Stop and get regulated immigration advice (OISC/solicitor).")
        return 1
    if left <= case.get("warn_days_left", 21):
        warnings.append(f"Only {left} days until permission expires on {expires}.")

    verified = case.get("rules_verified_on")
    max_rules_age = case.get("rules_max_age_days", 14)
    if not verified or (today - d(verified)).days > max_rules_age:
        blockers.append(f"Rules/fees last verified {verified or 'never'}. Re-check gov.uk and set rules_verified_on (max {max_rules_age} days).")

    for idoc in case.get("ids", []):
        if d(idoc["expires"]) <= today:
            blockers.append(f"{idoc['label']} expired on {idoc['expires']}.")

    for r in case.get("required", []):
        hits = [f for f in files(r["folder"]) if r["contains"].lower() in f.name.lower()
                and (not r.get("suffix") or f.suffix.lower() == r["suffix"])]
        uploads += hits
        if not hits:
            blockers.append(f"Missing: {r['label']} ({r['folder']}, name containing '{r['contains']}').")
    for r in case.get("recommended", []):
        hits = [f for f in files(r["folder"]) if r["contains"].lower() in f.name.lower()]
        uploads += hits
        if not hits:
            warnings.append(f"Recommended, not found: {r['label']}.")

    for fr in case.get("fresh", []):
        found = dated(fr["folder"], fr["pattern"])
        blockers += check_fresh(today, fr["label"], found, fr["max_age_days"])

    for s in case.get("series", []):
        found = dated(s["folder"], s["pattern"])
        ranges = None
        if s.get("covered_by"):
            rx = re.compile(s["covered_by"]["pattern"], re.I)
            ranges = [(d(m["start"]), d(m["end"])) for f in files(s["covered_by"]["folder"]) if (m := rx.search(f.name))]
            uploads += [f for f in files(s["covered_by"]["folder"]) if rx.search(f.name)]
        b, window = check_series(s["label"], [dt for dt, _ in found], ranges, s["months"])
        blockers += b
        uploads += [f for dt, f in found if (dt.year, dt.month) in window]

    for folder in case.get("upload_whole_folders", []):
        uploads += files(folder)

    markers = case.get("placeholder_markers", ["TBD"])
    for rel in case.get("placeholder_files", []):
        blockers += [f"Unfilled: {ln}" for ln in placeholder_lines(rel, markers)]

    blockers += [f"Open risk: {r}" for r in case.get("open_risks", [])]

    print(f"Date checked: {today}. Permission expires {expires} ({left} days left).")
    print("\nRESULT: " + ("NO-GO" if blockers else "GO"))
    for title, rows in (("BLOCKERS", blockers), ("WARNINGS", warnings)):
        if rows:
            print(f"\n{title}:\n" + "\n".join(f"  - {r}" for r in rows))
    if not blockers:
        print("\nUPLOAD THESE FILES:\n" + "\n".join(f"  - {p.relative_to(ROOT)}" for p in sorted(set(uploads))))
    return 1 if blockers else 0


def selftest():
    assert last_months(date(2026, 2, 23), 3) == [(2025, 12), (2026, 1), (2026, 2)]
    pays = [date(2026, m, 23) for m in range(5, 11)]
    stmt = [(date(2026, 4, 1), date(2026, 10, 25))]
    assert check_series("Payslips", pays, stmt, 6) == ([], last_months(date(2026, 10, 23), 6))
    gap, _ = check_series("Payslips", [p for p in pays if p.month != 7], stmt, 6)
    assert gap == ["Payslips: missing 2026-07."], gap
    unc, _ = check_series("Payslips", pays, [(date(2026, 6, 1), date(2026, 10, 25))], 6)
    assert unc == ["Payslips: no statement covers 2026-05-23."], unc
    assert check_fresh(date(2026, 11, 20), "Payslip", [(date(2026, 10, 23), None)], 28) == []
    assert check_fresh(date(2026, 11, 21), "Payslip", [(date(2026, 10, 23), None)], 28)
    print("selftest ok")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        selftest()
        sys.exit()
    today = d(sys.argv[sys.argv.index("--today") + 1]) if "--today" in sys.argv else date.today()
    sys.exit(main(today, json.loads((HERE / "case.json").read_text())))
