#!/usr/bin/env python3
"""Compare the TEP variable dictionary against the authoritative teprob.f comments.

The script:
1. Downloads the original teprob.f source (or reuses a local copy if already present).
2. Parses the comment block that defines XMEAS(1) through XMEAS(41) and XMV(1) through XMV(12).
3. Parses the markdown dictionary in data_dictionary.md.
4. Compares descriptions and units entry by entry and writes a report.

No dictionary entries are changed by this script; it only reports mismatches.
"""

from __future__ import annotations
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Tuple
import urllib.request

ROOT = Path(__file__).resolve().parent
TEPROB_URL = "https://raw.githubusercontent.com/camaramm/tennessee-eastman-profBraatz/master/teprob.f"
TEPROB_PATH = ROOT.parent / "data" / "teprob.f"
LOCAL_TEPROB_PATH = Path("/tmp/teprob.f")
DICT_PATH = ROOT.parent / "docs" / "data_dictionary.md"
REPORT_PATH = ROOT.parent / "docs" / "dictionary_comparison_report.md"


def normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip()).lower()


def download_teprob() -> str:
    if TEPROB_PATH.exists():
        return TEPROB_PATH.read_text(encoding="utf-8", errors="replace")

    if LOCAL_TEPROB_PATH.exists():
        text = LOCAL_TEPROB_PATH.read_text(encoding="utf-8", errors="replace")
        TEPROB_PATH.write_text(text, encoding="utf-8")
        return text

    try:
        with urllib.request.urlopen(TEPROB_URL, timeout=60) as response:
            text = response.read().decode("utf-8", errors="replace")
    except Exception:
        completed = subprocess.run(
            ["curl", "-L", "--fail", "--silent", "--show-error", TEPROB_URL],
            capture_output=True,
            text=True,
            check=False,
        )
        if completed.returncode != 0:
            raise RuntimeError(f"Unable to download teprob.f: {completed.stderr.strip()}")
        text = completed.stdout

    TEPROB_PATH.write_text(text, encoding="utf-8")
    return text


def parse_teprob(text: str) -> Dict[str, Dict[str, str]]:
    entries: Dict[str, Dict[str, str]] = {}
    for line in text.splitlines():
        line = line.rstrip()
        m = re.match(r"^\s*C\s+X(MEAS|MV)\((\d+)\)\s*(.*)$", line)
        if not m:
            continue

        kind = m.group(1)
        idx = int(m.group(2))
        rest = m.group(3).strip()
        if not rest:
            continue

        # For XMV lines, the source includes a note like "(Corrected Order)".
        # Remove that suffix so the description is closer to the dictionary meaning.
        if kind == "MV":
            rest = re.sub(r"\s*\(Corrected Order\)\s*$", "", rest).strip()
            description = rest
            unit = ""
        else:
            # Split the source line into description + unit at the last run of 3+ spaces.
            # This avoids breaking the description text itself, which may contain double spaces.
            split = re.split(r"\s{3,}", rest)
            if len(split) >= 2:
                description = split[0].strip()
                unit = split[-1].strip()
            else:
                description = rest
                unit = ""

        key = f"x{'meas' if kind == 'MEAS' else 'mv'}_{idx}"
        entries[key] = {
            "description": description,
            "unit": unit,
            "source": f"teprob.f:{kind}({idx})",
        }

    return entries


def parse_dictionary(text: str) -> Dict[str, Dict[str, str]]:
    rows: Dict[str, Dict[str, str]] = {}
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if len(cells) < 3:
            continue
        code = cells[0].strip("`")
        if not code.startswith("xmeas_") and not code.startswith("xmv_"):
            continue
        description = cells[1]
        unit = cells[2]
        rows[code] = {
            "description": description,
            "unit": unit,
            "source": "data_dictionary.md",
        }
    return rows


def compare_entries(teprob_entries: Dict[str, Dict[str, str]], dict_entries: Dict[str, Dict[str, str]]) -> Tuple[List[Dict[str, str]], List[str], List[str]]:
    mismatches: List[Dict[str, str]] = []
    missing_from_dict: List[str] = []
    missing_from_teprob: List[str] = []

    all_codes = sorted(set(teprob_entries) | set(dict_entries))
    for code in all_codes:
        teprob_entry = teprob_entries.get(code)
        dict_entry = dict_entries.get(code)

        if teprob_entry is None:
            missing_from_teprob.append(code)
            continue
        if dict_entry is None:
            missing_from_dict.append(code)
            continue

        desc_match = normalize(teprob_entry["description"]) == normalize(dict_entry["description"])
        unit_match = (not teprob_entry["unit"].strip()) or (normalize(teprob_entry["unit"]) == normalize(dict_entry["unit"]))
        if not (desc_match and unit_match):
            mismatches.append(
                {
                    "code": code,
                    "dict_description": dict_entry["description"],
                    "dict_unit": dict_entry["unit"],
                    "teprob_description": teprob_entry["description"],
                    "teprob_unit": teprob_entry["unit"],
                }
            )

    return mismatches, missing_from_dict, missing_from_teprob


def write_report(mismatches: List[Dict[str, str]], missing_from_dict: List[str], missing_from_teprob: List[str], teprob_entries: Dict[str, Dict[str, str]], dict_entries: Dict[str, Dict[str, str]]) -> None:
    lines: List[str] = []
    lines.append("# TEP variable dictionary comparison report")
    lines.append("")
    lines.append("This report compares the variable mappings in data_dictionary.md against the authoritative variable list in teprob.f.")
    lines.append("")
    lines.append(f"- Source file parsed: {TEPROB_PATH.name}")
    lines.append(f"- Dictionary file parsed: {DICT_PATH.name}")
    lines.append(f"- Entries checked from the dictionary: {len(dict_entries)}")
    lines.append(f"- Authoritative entries from teprob.f: {len(teprob_entries)}")
    lines.append(f"- Mismatches found: {len(mismatches)}")
    lines.append("")
    lines.append("## Mismatches")
    lines.append("")
    if mismatches:
        lines.append("| Variable | data_dictionary.md | teprob.f |")
        lines.append("|---|---|---|")
        for item in mismatches:
            dict_value = f"Description: {item['dict_description']}  Unit: {item['dict_unit']}"
            teprob_value = f"Description: {item['teprob_description']}  Unit: {item['teprob_unit']}"
            lines.append(f"| {item['code']} | {dict_value} | {teprob_value} |")
    else:
        lines.append("No mismatches were found.")
    lines.append("")
    lines.append("## Variables present in one file but missing in the other")
    lines.append("")
    if missing_from_dict:
        lines.append("### Missing from data_dictionary.md")
        lines.append(", ".join(missing_from_dict))
    else:
        lines.append("None")
    lines.append("")
    if missing_from_teprob:
        lines.append("### Missing from teprob.f")
        lines.append(", ".join(missing_from_teprob))
    else:
        lines.append("None")
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    text = download_teprob()
    teprob_entries = parse_teprob(text)
    dict_text = DICT_PATH.read_text(encoding="utf-8")
    dict_entries = parse_dictionary(dict_text)
    mismatches, missing_from_dict, missing_from_teprob = compare_entries(teprob_entries, dict_entries)
    write_report(mismatches, missing_from_dict, missing_from_teprob, teprob_entries, dict_entries)

    print(f"Parsed {len(teprob_entries)} authoritative entries from teprob.f")
    print(f"Parsed {len(dict_entries)} dictionary entries from data_dictionary.md")
    print(f"Found {len(mismatches)} mismatches")
    print(f"Report written to {REPORT_PATH}")

    if mismatches:
        for item in mismatches:
            print("-", item["code"])
            print("  dict:", item["dict_description"], "|", item["dict_unit"])
            print("  teprob:", item["teprob_description"], "|", item["teprob_unit"])

    if missing_from_dict:
        print("Missing from data_dictionary.md:", ", ".join(missing_from_dict))
    if missing_from_teprob:
        print("Missing from teprob.f:", ", ".join(missing_from_teprob))


if __name__ == "__main__":
    main()
