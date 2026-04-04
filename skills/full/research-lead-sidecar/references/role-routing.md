# Role Routing

Use this file when deciding **whether** to delegate and **which** sidecar role fits the task.

## Quick Table

| Role | Use When | Typical Output | Avoid When |
|---|---|---|---|
| Scout | You need evidence, landscape, comparisons, or codebase reconnaissance | notes, source table, shortlist, open questions | the next step depends on live back-and-forth reasoning |
| Worker | The task has a bounded write scope or a mechanical execution target | patch, script, run result, table, isolated artifact | write scope overlaps the lead or another worker |
| Verifier | A milestone, merge, or risky claim needs an independent check | prioritized findings, risk summary, go/no-go notes | every tiny subtask return |
| Writer | You need polished prose or structured summaries from accepted facts | report draft, summary, response text | the output requires net-new evidence gathering |

## Lead

The lead is not a sidecar.

The lead owns:
- problem framing
- critical path decisions
- accepted state
- synthesis across sidecars
- final claims

Keep the lead local when:
- the reasoning is sequential
- the tradeoff is central to the whole task
- a wrong answer would poison every downstream step

## Scout

Give a task to Scout when you need:
- literature or source collection
- official-doc comparison
- codebase reconnaissance
- benchmark or prior-art mapping
- shortlist creation before deeper work

Scout should return:
- what space was searched
- what looks relevant
- what is weak, missing, or stale
- what the lead should inspect next

Scout should not decide the final direction.

## Worker

Give a task to Worker when:
- the write scope is explicit
- the artifact is inspectable
- the lead can keep moving without waiting

Worker ownership must include:
- files or modules allowed to change
- files or modules explicitly out of scope
- local validation expected before return

Always say:
- "You are not alone in the codebase."
- "Do not revert others' edits."
- "Adjust to concurrent changes if they appear."

## Verifier

Use Verifier at:
- milestone boundaries
- risky merges
- before final claims
- when a sidecar's output may have hidden regressions or unsupported claims

Verifier should focus on:
- correctness
- regression risk
- claim-evidence alignment
- unverified areas

Verifier is a checkpoint, not a permanent bottleneck.

## Writer

Use Writer when:
- the facts already exist
- the output needs better structure or polish
- you want a reader-facing artifact without taking the lead off the technical path

Writer should state:
- target audience
- what evidence it relied on
- what still needs verification

Writer should not invent facts to make prose flow better.
