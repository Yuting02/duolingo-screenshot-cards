# Screenshot-To-Card Workflow

Use this reference for full runs that start from Duolingo screenshots.

## Inputs

- Use `screenshot/` for source images when present.
- Use `example/` only as a format contract or to confirm an occluded repeated word, not as extra vocabulary source.
- Write deliverables under `outputs/`.

## Screenshot Ordering

1. Use an explicit order from the user if provided.
2. If screenshot filenames are meaningful, use natural filename order.
3. If filenames are hashes or random names, inspect file creation/modified times and the visible scroll overlap.
4. Within each screenshot, read cards from top to bottom.
5. When two screenshots overlap, keep the first occurrence of a duplicate word and drop later duplicates.

## Extraction To `1duolingo.csv`

Create UTF-8 CSV with exactly:

```csv
法语单词,英文翻译
```

Rules:

- Use bold dark text as `法语单词`.
- Use the gray line below it as `英文翻译`.
- Preserve original accents, apostrophes, spaces, and hyphens.
- Keep Duolingo's visible English translation, even when it is awkward.
- Do not add extra columns.
- Flag uncertain OCR or hidden text before guessing.
- If a bottom row is obscured by the app navigation bar, include it only when the word and translation are both visible or the missing translation is confirmed by provided project examples.

## Enrichment To `2英标例句.csv`

Create UTF-8 CSV with exactly:

```csv
法语单词,法语英标,例句,词性/用法,英文翻译,中文翻译
```

Use `references/enrichment-guidelines.md` for field-level rules.

## Card Rendering To `3卡片.txt`

Render from `outputs/2英标例句.csv`, not from memory. Use:

```bash
python <skill-dir>/scripts/render_cards.py --input <workspace>/outputs/2英标例句.csv --output <workspace>/outputs/3卡片.txt
```

Validate after rendering:

```bash
python <skill-dir>/scripts/validate_outputs.py --root <workspace>
```