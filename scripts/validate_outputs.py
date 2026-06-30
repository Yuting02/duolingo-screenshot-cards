#!/usr/bin/env python3
"""Validate Duolingo screenshot-card workflow outputs."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


STAGE1_HEADERS = ["法语单词", "英文翻译"]
STAGE2_HEADERS = ["法语单词", "法语英标", "例句", "词性/用法", "英文翻译", "中文翻译"]


def read_csv(path: Path) -> tuple[list[str], list[list[str]]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        rows = list(reader)
    if not rows:
        raise SystemExit(f"empty CSV: {path}")
    return rows[0], rows[1:]


def validate(root: Path) -> dict[str, object]:
    outputs = root / "outputs"
    stage1 = outputs / "1duolingo.csv"
    stage2 = outputs / "2英标例句.csv"
    cards = outputs / "3卡片.txt"

    for path in (stage1, stage2, cards):
        if not path.exists():
            raise SystemExit(f"missing output: {path}")

    headers1, rows1 = read_csv(stage1)
    headers2, rows2 = read_csv(stage2)
    if headers1 != STAGE1_HEADERS:
        raise SystemExit(f"unexpected 1duolingo.csv headers: {headers1}")
    if headers2 != STAGE2_HEADERS:
        raise SystemExit(f"unexpected 2英标例句.csv headers: {headers2}")
    if not all(len(row) == len(STAGE1_HEADERS) for row in rows1):
        raise SystemExit("1duolingo.csv has rows with wrong column count")
    if not all(len(row) == len(STAGE2_HEADERS) for row in rows2):
        raise SystemExit("2英标例句.csv has rows with wrong column count")

    text = cards.read_text(encoding="utf-8-sig")
    card_count = text.count("[P#H1#")
    end_count = text.count("*****")
    if len(rows1) != len(rows2):
        raise SystemExit(f"row count mismatch: 1duolingo={len(rows1)} 2英标例句={len(rows2)}")
    if len(rows2) != card_count or card_count != end_count:
        raise SystemExit(f"card count mismatch: rows2={len(rows2)} cards={card_count} markers={end_count}")

    return {
        "stage1_rows": len(rows1),
        "stage2_rows": len(rows2),
        "cards": card_count,
        "end_markers": end_count,
        "ok": True,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate Duolingo card workflow outputs.")
    parser.add_argument("--root", required=True, type=Path, help="Workspace root containing outputs/")
    args = parser.parse_args()
    print(json.dumps(validate(args.root), ensure_ascii=True))


if __name__ == "__main__":
    main()