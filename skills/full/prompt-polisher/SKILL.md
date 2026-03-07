---
name: prompt-polisher
description: Use when receiving messy, unstructured input like voice transcriptions, stream-of-consciousness notes, or rough document content that needs to be transformed into a polished, optimized prompt. Cleans up filler words, extracts intent, asks clarifying questions, applies Claude 4.x/Opus 4.5/Sonnet 4.5 best practices, and previews the polished prompt for approval before execution. Trigger phrases include "polish this", "clean this up", "turn this into a prompt", or when input is clearly rough/unstructured.
---

# Prompt Polisher

Transform messy, unstructured input into polished, Claude-optimized prompts using Anthropic's best practices.

## When to Activate

Activate this skill when:
- User provides voice transcription content (contains filler words, self-corrections, casual speech)
- User dumps stream-of-consciousness notes
- User pastes rough document content that needs structuring
- User explicitly asks to "polish", "clean up", or "turn this into a prompt"
- Input is clearly unstructured and intended as task instructions

## Workflow

Execute these stages in order:

### Stage 1: Voice Cleanup

If the input appears to be voice transcription or casual speech, clean it up:

**Remove:**
- Filler words: "um", "uh", "like", "you know", "basically", "actually", "literally", "right?"
- Self-corrections: "no wait", "I mean", "actually scratch that", "let me rephrase"
- False starts: repeated or abandoned sentence beginnings
- Verbal tics: "okay so", "let me think", "hmm"

**Normalize:**
- Convert spoken patterns to written form
- Fix run-on sentences
- Add proper punctuation

### Stage 2: Intent Extraction

Parse the cleaned input to identify:

| Element | What to Find |
|---------|--------------|
| Core task | What does the user actually want done? |
| Referenced files | Documents, project files, URLs mentioned |
| Constraints | Limitations, requirements, boundaries |
| Preferences | Style, format, approach preferences |
| Success criteria | What does "done" look like? |
| Scope | Single task vs. multi-step project |

### Stage 3: Gap Detection

Scan for missing or ambiguous elements:

- [ ] Ambiguous requirements ("process them somehow")
- [ ] Missing success criteria (no clear definition of "done")
- [ ] Unclear scope (single task or multi-step?)
- [ ] Format unspecified (code? prose? structured output?)
- [ ] Model unknown (Opus 4.5 or Sonnet 4.5?)
- [ ] Technical choices undefined (which library/approach/pattern?)

**If gaps exist, ask ALL clarifying questions at once:**

```
Before I polish this prompt, I need to clarify a few things:

1. [First gap-specific question]
2. [Second gap-specific question]
3. Which Claude model are you using? (Opus 4.5 / Sonnet 4.5 / Not sure)
```

Wait for user response before proceeding.

### Stage 4: Apply Best Practices

Reference [reference.md](reference.md) for detailed guidelines. Apply these transformations:

**Universal (Claude 4.x):**
- Make instructions explicit and direct (no hints)
- Add contextual framing (explain WHY, not just WHAT)
- Use positive framing ("use prose" not "don't use bullets")
- Structure with XML tags for complex inputs
- Use action-oriented language ("Change this" not "Can you suggest")
- Include chain of thought prompts for complex reasoning
- Define clear success criteria
- Use normal tone (avoid aggressive CAPS/MUST/CRITICAL)

**If Opus 4.5:**
- Add anti-over-engineering guardrail: "Keep solutions simple. Only make changes directly requested."
- Avoid the word "think" → use "consider", "evaluate", "believe"
- Leverage planning strength: "Build an editable plan before executing"
- Keep prompts token-efficient (don't over-pad)
- Provide policy/constraint context when relevant

**If Sonnet 4.5:**
- Break complex tasks into explicit steps
- Optimize for speed/throughput
- Add more explicit step-by-step guidance for intricate tasks

### Stage 5: Structure the Prompt

Generate the polished prompt using this template:

```xml
<context>
[Background info, relevant project context, referenced files, WHY this task matters]
</context>

<task>
[Clear, explicit statement of what needs to be done - action-oriented]
</task>

<requirements>
[Specific constraints, boundaries, must-haves, technical choices]
</requirements>

<success_criteria>
[What "done" looks like, how to verify completion]
</success_criteria>

<approach>  <!-- Optional: include for complex tasks -->
[Suggested approach OR "Build an editable plan before executing"]
</approach>
```

**Formatting rules:**
- Keep each section focused and concise
- Use bullet points only when listing multiple items
- Omit sections that aren't relevant to the task
- For simple tasks, a streamlined version without XML tags is acceptable

### Stage 6: Preview for Approval

Present the polished prompt to the user:

```
Here's your polished prompt:

---

[POLISHED PROMPT CONTENT]

---

**Options:**
- **Execute** - Run this prompt now
- **Edit** - I'll modify something first
- **Redo** - Start over with different clarifications
```

**Wait for user approval before executing.**

### Stage 7: Execute or Iterate

Based on user choice:
- **Execute**: Immediately act on the polished prompt as if the user had typed it directly
- **Edit**: User modifies the prompt, then re-preview
- **Redo**: Return to Stage 1 with new input or Stage 3 for new clarifications

## Important Notes

- Always preview before executing - never skip the approval step
- If the input is already well-structured, acknowledge this and offer minor polish only
- Learn from user feedback - if they frequently edit a certain way, note the pattern
- For very short/simple inputs, use a streamlined format without full XML structure
- The goal is USEFUL prompts, not LONG prompts - be concise

## See Also

- [reference.md](reference.md) - Detailed Anthropic best practices for Claude 4.x, Opus 4.5, and Sonnet 4.5
- [examples.md](examples.md) - Before/after transformation examples
