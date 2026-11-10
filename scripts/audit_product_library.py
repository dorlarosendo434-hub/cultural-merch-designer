#!/usr/bin/env python3
"""Validate the maintained product-material library."""

from __future__ import annotations

import re
import sys
from pathlib import Path


ROW = re.compile(r"^\|\s*([A-H]\d{2})\s*\|(.+?)\|(.+?)\|(.+?)\|(.+?)\|\s*(低|低中|中|中高|高)\s*\|$")


def main() -> int:
    skill_dir = Path(__file__).resolve().parents[1]
    library = skill_dir / "references" / "product-material-library.md"
    rows: list[tuple[str, ...]] = []

    for line in library.read_text(encoding="utf-8").splitlines():
        match = ROW.match(line)
        if match:
            rows.append(tuple(part.strip() for part in match.groups()))

    errors: list[str] = []
    ids = [row[0] for row in rows]
    combos = [row[1:5] for row in rows]

    if len(rows) < 40:
        errors.append(f"expected at least 40 combinations, found {len(rows)}")
    if len(ids) != len(set(ids)):
        errors.append("duplicate combination IDs found")
    if len(combos) != len(set(combos)):
        errors.append("duplicate product/material/process/interaction combinations found")

    expected_ids = {f"{family}{index:02d}" for family in "ABCDEFGH" for index in range(1, 7)}
    missing = sorted(expected_ids - set(ids))
    extra = sorted(set(ids) - expected_ids)
    if missing:
        errors.append(f"missing IDs: {', '.join(missing)}")
    if extra:
        errors.append(f"unexpected IDs: {', '.join(extra)}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print(f"OK: {len(rows)} unique combinations across 8 product families")
    return 0


if __name__ == "__main__":
    sys.exit(main())
