---
name: skills-governance
description: Use when auditing a large local skill collection, identifying duplicate or imported skills, comparing skill roots, or deciding what to keep, disable, or archive across Codex and adjacent agent skill directories.
user-invocable: true
---

# Skills Governance

## Purpose

Use the bundled scanner as the source of truth for local skill inventory. Base recommendations on real directories and `SKILL.md` frontmatter instead of stale catalogs or memory.

## When to Use

- The user says they have too many skills and cannot tell what is useful.
- The user wants a Codex-first keep or disable plan.
- The user needs duplicate-name groups across multiple skill roots.
- The user suspects imported plugin packs or mirrored skills are causing confusion.
- The user wants a filesystem-backed inventory before changing skill settings.

## How to Run It

Invoke the bundled `scan.js` from this skill directory.

- Codex-first inventory: `node scan.js --mode codex --format markdown`
- Cross-agent inventory: `node scan.js --mode all --format markdown`
- Duplicate review only: `node scan.js --mode all --duplicates-only --format markdown`
- Machine-readable output: `node scan.js --mode all --format json`

## Workflow

1. Run the scanner in `codex` mode first.
2. If the results still do not explain the user's confusion, rerun in `all` mode.
3. Explain the problem from roots, duplicate groups, and suspicious flags before recommending changes.
4. Prefer Codex `[[skills.config]]` disable suggestions over editing individual `SKILL.md` files unless the user explicitly asks for direct file edits.
5. Separate recommendations into three buckets: keep, disable for now, and archive or external mirror.
6. If the user asks to execute changes, list exact target paths and wait for confirmation first.

## Output Contract

Report at least:

- scanned roots
- total skills
- enabled and disabled counts
- duplicate-name groups
- suspicious flags such as `plugin-import`, `system`, or `backup-like`
- a compact per-skill list when needed

## Acceptance

A good run:

- completes without external dependencies
- reflects the actual filesystem state
- shows duplicate groups by skill `name`
- remains stable across repeated runs unless files changed
