# Card Format Contract

Use this reference when writing or checking `outputs/3卡片.txt`.

## Required Input CSV

`outputs/2英标例句.csv` must contain:

```csv
法语单词,法语英标,例句,词性/用法,英文翻译,中文翻译
```

The script also accepts `词性用法` as a legacy alias for `词性/用法`.

## One Card

```text
[P#H1#法语单词]
---
法语单词

[法语英标]

✅法语例句。
-- English sentence.
⭐词性/用法
-- English translation; 中文翻译
*****
```

## Rules

- Generate exactly one card per enriched CSV row.
- Preserve row order.
- Keep one blank line between cards.
- Use the French word exactly in both the `[P#H1#...]` title and the body word line.
- Do not regenerate examples or translations while rendering cards; use CSV values.
- End every card with `*****`.