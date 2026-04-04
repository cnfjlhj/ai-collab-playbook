---
name: research-lead-sidecar
description: Use when the user wants multi-agent division of labor for research-led work and the lead should stay on the critical path while 1-2 bounded sidecars handle low-coupling tasks. Do not use this for tiny tasks, fully sequential debugging, or overlapping refactors.
---

# Research Lead Sidecar

## Overview

Use this skill for research-led work where implementation and evidence gathering are coupled, but the main agent should remain the lead. It keeps the critical path local while bounded sidecars handle non-blocking scout, worker, verifier, or writer tasks.

## Rules

- Keep the lead responsible for framing, synthesis, and final decisions.
- Delegate only tasks that are non-blocking, bounded, inspectable, and recoverable.
- Prefer 1-2 sidecars with clear roles instead of spawning a crowd by default.
- The lead should keep moving on the critical path instead of waiting idly for sidecars.
- Use milestone verification and durable workspace state only when the task span justifies them.

## When to Use

Use when:

- the user explicitly wants 多智能体分工, research-led multi-agent work, or long-task governance with a lead agent
- there is one critical path plus a small number of low-coupling side tasks
- sidecars can return artifacts the lead can inspect quickly

Do not use when:

- the task is tiny, fully sequential, or blocked on each previous result
- several agents would need to touch the same hot files or same narrow context
- handoff cost is higher than simply doing the work locally
