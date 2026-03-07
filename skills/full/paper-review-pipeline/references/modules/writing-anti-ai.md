# Module: Writing Anti-AI (De-Slop / Humanize) — Feature-Parity Import

This module preserves the distinctive “anti-AI writing patterns” approach from the legacy `writing-anti-ai` skill.

## Core Rules (Must Support)

1) Cut filler phrases (throat-clearing openers, emphasis crutches).
2) Break formulaic structures (forced binary contrasts, rule-of-three, excessive em-dashes).
3) Vary rhythm (sentence and paragraph length variety).
4) Trust readers (state facts directly; remove hand-holding).
5) Cut “quotables” (rewrite anything that sounds like a pull-quote).

## Pattern Taxonomy (Must Support)

Detect and fix:
- Undue emphasis / inflated symbolism (“stands as a testament”, “crucial role”)
- Promotional language (“breathtaking”, “vibrant”, etc.)
- Vague attributions (“experts believe” without naming a source)
- Superficial “-ing” analysis chains (“highlighting… ensuring…”)
- AI vocabulary overuse (“Additionally”, “delve”, “landscape”, etc.)
- Negative parallelisms (“not just X, but Y”)
- Elegant variation overuse (synonym churn)

Support both English and Chinese rewriting.

## Workflow (Must Support)

1) Identify patterns in the provided text.
2) Rewrite while preserving meaning and tone requirements.
3) Ensure technical terminology is not altered without confirmation.
4) Optionally add voice if the user wants it (avoid sterile neutrality).

## Quick Scoring Rubric (Must Support)

Score 1–10 each:
- Directness
- Rhythm
- Trust (respects reader intelligence)
- Authenticity
- Density (cuttable content)

Total out of 50; provide interpretation if asked.

## Notes on “No-Omission” Parity

The legacy skill contains extensive pattern lists and examples. If the user requests the full catalog, load the legacy reference files (if present in the environment) and apply them:
- `~/.codex/skills/writing-anti-ai/SKILL.md`

(The skill may be disabled for auto-invocation, but its content remains available for reference.)

