---
name: duolingo-screenshot-cards
description: Convert Duolingo "Words" screenshots into French vocabulary study-card artifacts. Use when the user asks to extract French words from Duolingo screenshots, generate `1duolingo.csv`, enrich words with French IPA, examples, usage notes, English and Chinese translations in `2英标例句.csv`, or render `[P#H1#word]` TXT cards such as `3卡片.txt`; also use for the local Duolingo-momo-word screenshot-to-card workflow.
---

# Duolingo Screenshot Cards

## Overview

Produce three files from Duolingo vocabulary screenshots: a raw extraction CSV, an enriched learning CSV, and a final TXT card deck. Preserve screenshot order, preserve original words/translations, and use scripts for deterministic card rendering and validation.

## Workflow

1. Locate inputs. If the user gives a workspace, use its `screenshot/`, `example/`, and `outputs/` folders when present. Preserve originals and create `outputs/` if needed.
2. Read `references/workflow.md` before a full screenshot-to-card run. It defines screenshot ordering, duplicate handling, OCR ambiguity handling, and output file names.
3. Extract visible French word rows into `outputs/1duolingo.csv`.
4. Read `references/enrichment-guidelines.md`, then create `outputs/2英标例句.csv` with IPA, a natural example, usage notes, English translation, and Chinese translation.
5. Read `references/card-format.md`, then render `outputs/3卡片.txt`. Prefer the bundled script:

```bash
python <skill-dir>/scripts/render_cards.py --input <workspace>/outputs/2英标例句.csv --output <workspace>/outputs/3卡片.txt
```

6. Validate the package:

```bash
python <skill-dir>/scripts/validate_outputs.py --root <workspace>
```

## Image Extraction Rules

- Treat screenshots as source data, not decorative references.
- Read visible rows top-to-bottom in the actual scroll order. If filenames are hashes, prefer creation/modified time; if user gives an explicit order, use that order.
- The bold dark text is the French word or phrase. The gray line below is the Duolingo English translation.
- Remove duplicates after extraction while preserving the first occurrence.
- Do not guess hidden or cut-off rows. If a row is partially covered, include it only when both the word and translation are clear, or when the missing part can be confirmed from a provided example/output file; disclose that fallback.
- If local image preview fails, use another available visual path such as browser display or image emission. Do not invent OCR text.

## Outputs

- `outputs/1duolingo.csv`: columns `法语单词,英文翻译`.
- `outputs/2英标例句.csv`: columns `法语单词,法语英标,例句,词性/用法,英文翻译,中文翻译`.
- `outputs/3卡片.txt`: one `[P#H1#...]` card per enriched CSV row, ending each card with `*****`.

## Scripts

- `scripts/render_cards.py`: render the enriched CSV into final TXT cards and optionally run a no-write check.
- `scripts/validate_outputs.py`: validate expected files, headers, row counts, and card marker counts.

Run scripts with UTF-8 capable Python. On Windows PowerShell, prefer the bundled Codex Python when available or set `PYTHONUTF8=1` if console encoding causes mojibake.

## Quality Bar

- Never output only instructions when the user asked for generated cards; create the files.
- Keep source order stable across all three files.
- Keep French accents and IPA symbols intact.
- Keep English translations short in the enriched CSV, ideally 1-3 words.
- Use Chinese-only explanations in `中文翻译` and beginner-friendly Chinese in `词性/用法`.
- Verify counts before finishing: extracted rows, enriched rows, and cards should match unless a discrepancy is explicitly explained.