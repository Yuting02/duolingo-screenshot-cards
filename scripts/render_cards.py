#!/usr/bin/env python3
"""Render Duolingo enriched CSV rows into TXT study cards."""

from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path


REQUIRED_HEADERS = ["法语单词", "法语英标", "例句", "英文翻译", "中文翻译"]
USAGE_HEADERS = ("词性/用法", "词性用法")


def read_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise SystemExit(f"empty CSV: {path}")

        headers = set(reader.fieldnames)
        missing = [name for name in REQUIRED_HEADERS if name not in headers]
        if missing:
            raise SystemExit(f"missing required columns: {', '.join(missing)}")
        if not any(name in headers for name in USAGE_HEADERS):
            raise SystemExit("missing required column: 词性/用法")

        rows = []
        for index, row in enumerate(reader, start=2):
            clean = {key: (value or "").strip() for key, value in row.items()}
            if not clean.get("法语单词"):
                raise SystemExit(f"blank 法语单词 at CSV row {index}")
            rows.append(clean)
        return rows


def usage_value(row: dict[str, str]) -> str:
    for key in USAGE_HEADERS:
        value = row.get(key, "").strip()
        if value:
            return value
    return ""


def render_card(row: dict[str, str]) -> str:
    word = row["法语单词"].strip()
    ipa = row["法语英标"].strip()
    example = row["例句"].strip()
    usage = usage_value(row)
    english = row["英文翻译"].strip()
    chinese = row["中文翻译"].strip()

    if not ipa.startswith("[") or not ipa.endswith("]"):
        raise SystemExit(f"IPA must keep square brackets for {word}: {ipa}")
    if not example:
        raise SystemExit(f"missing example for {word}")
    if not usage.startswith("⭐"):
        raise SystemExit(f"usage must start with ⭐ for {word}")

    return "\n".join(
        [
            f"[P#H1#{word}]",
            "---",
            word,
            "",
            ipa,
            "",
            example,
            usage,
            f"-- {english}; {chinese}",
            "*****",
        ]
    )


def render_cards(rows: list[dict[str, str]]) -> str:
    return "\n\n".join(render_card(row) for row in rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Render Duolingo enriched CSV into TXT cards.")
    parser.add_argument("--input", required=True, type=Path, help="Path to 2英标例句.csv")
    parser.add_argument("--output", type=Path, help="Path to write 3卡片.txt")
    parser.add_argument("--check", action="store_true", help="Validate and render in memory without requiring output.")
    args = parser.parse_args()

    rows = read_rows(args.input)
    text = render_cards(rows)

    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text + "\n", encoding="utf-8", newline="\n")
    elif not args.check:
        raise SystemExit("provide --output or --check")

    print(json.dumps({"rows": len(rows), "cards": text.count("[P#H1#")}, ensure_ascii=True))


if __name__ == "__main__":
    main()