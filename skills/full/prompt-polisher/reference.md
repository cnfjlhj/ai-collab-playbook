# Anthropic Best Practices Reference

This document contains prompt engineering guidelines from Anthropic's official documentation for Claude 4.x models, including Opus 4.5 and Sonnet 4.5.

**Sources:**
- [Claude 4 Prompt Engineering Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-4-best-practices)
- [Prompt Engineering Overview](https://platform.claude.com/docs/en/docs/build-with-claude/prompt-engineering/overview)
- [Introducing Claude Opus 4.5](https://www.anthropic.com/news/claude-opus-4-5)

---

## Core Principles (All Claude 4.x Models)

### 1. Explicit Instructions

Be direct and specific. Don't assume Claude will infer what you want.

| Instead of | Use |
|------------|-----|
| "Create a dashboard" | "Create an analytics dashboard with filtering, sorting, and export functionality. Include interactive charts." |
| "Make it better" | "Improve the performance by reducing database queries and adding caching for repeated operations." |
| "Help me with this code" | "Refactor this function to use async/await instead of callbacks, and add error handling for network failures." |

### 2. Contextual Framing

Explain the reasoning behind requests. The "why" helps Claude make better decisions.

| Instead of | Use |
|------------|-----|
| "Never use ellipses" | "Your response will be read aloud by text-to-speech, so avoid ellipses which create awkward pauses." |
| "Keep it short" | "This will be displayed on mobile screens with limited space, so keep responses under 100 words." |
| "Use simple language" | "The audience is non-technical stakeholders, so avoid jargon and explain concepts in plain terms." |

### 3. Positive Framing

Specify what you want, not what you don't want.

| Instead of | Use |
|------------|-----|
| "Don't use markdown" | "Use flowing prose paragraphs without special formatting" |
| "Don't be verbose" | "Be concise and direct" |
| "Don't include unnecessary details" | "Focus only on the core functionality" |

### 4. Action-Oriented Language

Use direct action requests, not suggestions or questions.

| Instead of | Use |
|------------|-----|
| "Can you suggest changes?" | "Change this function to improve performance." |
| "Would it be possible to add...?" | "Add error handling for edge cases." |
| "Maybe we could try...?" | "Implement caching using Redis." |

### 5. XML Tags for Structure

Use XML tags to organize complex inputs and guide output format.

```xml
<context>
Background information and relevant details
</context>

<task>
The specific action to perform
</task>

<requirements>
Constraints and specifications
</requirements>

<output_format>
How the response should be structured
</output_format>
```

### 6. Normal Tone

Claude 4.x models are highly responsive to system prompts. Aggressive language is unnecessary and can cause over-triggering.

| Instead of | Use |
|------------|-----|
| "CRITICAL: You MUST always..." | "Always..." |
| "NEVER under ANY circumstances..." | "Avoid..." |
| "This is ABSOLUTELY ESSENTIAL..." | "This is important..." |

---

## Claude Opus 4.5 Specific

Opus 4.5 is Anthropic's most intelligent model, excelling at complex, long-horizon tasks and deep reasoning.

### Strengths
- State-of-the-art coding (80.9% SWE-bench)
- Long-horizon autonomous tasks
- Complex multi-step reasoning
- Handling ambiguity and tradeoffs independently
- Token-efficient (achieves more with fewer tokens)

### Known Tendencies

**Over-engineering:** Opus 4.5 tends to add unnecessary abstractions, extra files, or flexibility that wasn't requested.

**Mitigation:** Add explicit guardrails:
```
Keep solutions simple and focused. Only make changes that are directly requested or clearly necessary. Don't add features, refactor code, or make "improvements" beyond what was asked.
```

### Word Sensitivity

When extended thinking is disabled, Opus 4.5 is sensitive to the word "think" and its variants.

| Instead of | Use |
|------------|-----|
| "Think about..." | "Consider..." |
| "Think through..." | "Evaluate..." |
| "I think..." | "I believe..." |
| "Let me think..." | "Let me assess..." |

### Leverage Planning Strength

Opus excels when allowed to plan before executing:

```
Before implementing, build an editable plan that outlines:
1. The approach you'll take
2. Files that will be created or modified
3. Key decision points

Present the plan for approval before proceeding.
```

### Token Efficiency

Opus 4.5 is highly token-efficient. Don't over-pad prompts with unnecessary context or repetition. Be concise.

### Policy Context

When tasks require navigating constraints, explicitly state acceptable parameters:

```
You may use any standard library functions. Third-party dependencies require approval. Prefer built-in solutions when equivalent functionality exists.
```

---

## Claude Sonnet 4.5 Specific

Sonnet 4.5 is the balanced model - intelligent and fast, ideal for most everyday tasks.

### Strengths
- Excellent coding (72.7% SWE-bench)
- Fast response times
- High throughput
- Good balance of capability and efficiency
- Strong for chat, content, summaries

### Known Tendencies

**Can get stuck:** On extremely intricate tasks, Sonnet may struggle where Opus would navigate to an answer.

**Mitigation:** Break complex tasks into explicit steps:
```
Complete this task in these steps:
1. First, [specific action]
2. Then, [next action]
3. Finally, [concluding action]

Report progress after each step.
```

### When to Use Sonnet vs Opus

| Use Sonnet when... | Use Opus when... |
|-------------------|------------------|
| Task is straightforward | Task is deeply complex |
| Speed matters | Accuracy is critical |
| Wrong answer is cheap to fix | Wrong answer is expensive |
| High throughput needed | Deep reasoning required |
| Most everyday workflows | Research, enterprise, agents |

---

## Prompt Structure Template

For complex tasks, use this structure:

```xml
<context>
[Background: What is this project? What's the current state?]
[Why: Why does this task matter? What's the goal?]
[References: Relevant files, documents, or prior context]
</context>

<task>
[Clear, explicit, action-oriented statement of what to do]
</task>

<requirements>
[Technical constraints]
[Style/format preferences]
[Boundaries - what NOT to do]
[Dependencies or prerequisites]
</requirements>

<success_criteria>
[What does "done" look like?]
[How to verify the task is complete]
[Acceptance criteria]
</success_criteria>

<approach>
[Optional: Suggested approach]
[Or: "Build an editable plan before executing"]
</approach>
```

For simple tasks, a streamlined version works:

```
[One sentence of context if needed]

[Direct action statement]: [specific details]

[Key constraint or success criterion]
```

---

## Anti-Patterns to Avoid

### 1. Vague Instructions
```
Bad:  "Make it better"
Good: "Reduce response time by implementing caching for database queries"
```

### 2. Negative Framing
```
Bad:  "Don't write verbose code with lots of comments"
Good: "Write concise code with minimal comments, only where logic isn't self-evident"
```

### 3. Aggressive Tone
```
Bad:  "You MUST ALWAYS follow these rules EXACTLY or you will FAIL"
Good: "Follow these guidelines consistently"
```

### 4. Missing Context
```
Bad:  "Fix the bug"
Good: "Fix the null pointer exception in user authentication when email field is empty"
```

### 5. Ambiguous Scope
```
Bad:  "Improve the code"
Good: "Refactor the getUserData function to use async/await and add error handling"
```

---

## Quick Reference Card

| Principle | Do | Don't |
|-----------|-----|-------|
| Clarity | Be explicit and specific | Assume inference |
| Framing | Explain the why | Just state the what |
| Tone | Use normal language | Use aggressive CAPS |
| Structure | Use XML tags for complex tasks | Dump unstructured text |
| Action | Direct imperatives | Questions or suggestions |
| Scope | Define success criteria | Leave "done" undefined |
| Opus 4.5 | Add anti-over-engineering | Let it gold-plate |
| Sonnet 4.5 | Break into explicit steps | Give complex monoliths |
