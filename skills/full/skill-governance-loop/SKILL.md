---
name: skill-governance-loop
description: Use when the user asks to review a skill, analyze skill quality, update a skill version, or run a repeatable keep/disable/archive decision loop from real failures instead of abstract best practices.
---

# Skill Governance Loop

## Overview

Use this skill for evidence-based governance of one skill or a small target set. It starts from a concrete problem, audits the skill, and ends with an explicit keep, disable, merge, split, or archive decision.

## Rules

- Start from a concrete case such as poor triggering, overlap, bloat, or a version update request.
- Produce three outputs every time: the case, the audit, and the decision.
- Separate static quality from observed usefulness; a pretty skill is not automatically a useful skill.
- Use inventory tooling first when the scope is broad enough to need filesystem evidence.
- Record the next hypothesis so the next governance pass has a sharper starting point.

## When to Use

Use when:

- the user asks to review a skill, analyze skill quality, or update a skill version
- a skill may need to be kept, disabled, merged, split, archived, or moved
- the user wants a repeatable governance loop instead of one-off edits

Do not use when:

- the task is broad inventory scanning of many skills at once
- the work is simple skill authoring with no governance decision
- the request is only to discover whether a skill exists
