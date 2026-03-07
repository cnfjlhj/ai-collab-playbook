---
name: find-skills
description: Helps users discover and install agent skills when they ask questions like "how do I do X", "find a skill for X", "is there a skill that can...", or express interest in extending capabilities. Start with the skills.sh registry via `npx skills find`; if there are no good matches, fall back to a GitHub deep search for SKILL.md patterns before concluding no skill exists.
---

# Find Skills

This skill helps you discover and install skills from the open agent skills ecosystem.

## Default Workflow (Two-Stage)

1. **Search the registry first (fast + installable):** `npx skills find <query>`
2. **If found:** present top options + ask what to install
3. **If not found:** fall back to GitHub deep search (skill-hunter style) to discover skills that may not be indexed yet
4. **If still not found:** help the user directly, or propose creating a new skill

Notes:

- Prefer **non-interactive** usage in a coding agent: always pass a query (avoid `npx skills find` with no args).
- To disable Skills CLI telemetry, set `DISABLE_TELEMETRY=1` (or `DO_NOT_TRACK=1`) when running `npx skills ...`.

## When to Use This Skill

Use this skill when the user:

- Asks "how do I do X" where X might be a common task with an existing skill
- Says "find a skill for X" or "is there a skill for X"
- Asks "can you do X" where X is a specialized capability
- Expresses interest in extending agent capabilities
- Wants to search for tools, templates, or workflows
- Mentions they wish they had help with a specific domain (design, testing, deployment, etc.)

## What is the Skills CLI?

The Skills CLI (`npx skills`) is the package manager for the open agent skills ecosystem. Skills are modular packages that extend agent capabilities with specialized knowledge, workflows, and tools.

**Key commands:**

- `npx skills find [query]` - Search for skills interactively or by keyword
- `npx skills add <package>` - Install a skill from GitHub or other sources
- `npx skills check` - Check for skill updates
- `npx skills update` - Update all installed skills

**Browse skills at:** https://skills.sh/

## How to Help Users Find Skills

### Step 1: Understand What They Need

When a user asks for help with something, identify:

1. The domain (e.g., React, testing, design, deployment)
2. The specific task (e.g., writing tests, creating animations, reviewing PRs)
3. Whether this is a common enough task that a skill likely exists

### Step 2: Search for Skills

Run the find command with a relevant query:

```bash
DISABLE_TELEMETRY=1 npx -y skills find [query]
```

For example:

- User asks "how do I make my React app faster?" → `npx skills find react performance`
- User asks "can you help me with PR reviews?" → `npx skills find pr review`
- User asks "I need to create a changelog" → `npx skills find changelog`

The command will return results like:

```
Install with npx skills add <owner/repo@skill>

vercel-labs/agent-skills@vercel-react-best-practices
└ https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices
```

### Step 3: Present Options to the User

When you find relevant skills, present them to the user with:

1. The skill name and what it does
2. The install command they can run
3. A link to learn more at skills.sh

Example response:

```
I found a skill that might help! The "vercel-react-best-practices" skill provides
React and Next.js performance optimization guidelines from Vercel Engineering.

To install it:
npx skills add vercel-labs/agent-skills@vercel-react-best-practices

Learn more: https://skills.sh/vercel-labs/agent-skills/vercel-react-best-practices
```

### Step 4: Offer to Install

If the user wants to proceed, you can install the skill for them:

```bash
DISABLE_TELEMETRY=1 npx -y skills add <owner/repo@skill> -g --agent codex -y
```

The `-g` flag installs globally (user-level) and `-y` skips confirmation prompts.

## Common Skill Categories

When searching, consider these common categories:

| Category        | Example Queries                          |
| --------------- | ---------------------------------------- |
| Web Development | react, nextjs, typescript, css, tailwind |
| Testing         | testing, jest, playwright, e2e           |
| DevOps          | deploy, docker, kubernetes, ci-cd        |
| Documentation   | docs, readme, changelog, api-docs        |
| Code Quality    | review, lint, refactor, best-practices   |
| Design          | ui, ux, design-system, accessibility     |
| Productivity    | workflow, automation, git                |

## Tips for Effective Searches

1. **Use specific keywords**: "react testing" is better than just "testing"
2. **Try alternative terms**: If "deploy" doesn't work, try "deployment" or "ci-cd"
3. **Check popular sources**: Many skills come from `vercel-labs/agent-skills` or `ComposioHQ/awesome-claude-skills`

## When No Skills Are Found

If no relevant skills are found in the registry, do a quick GitHub deep search before concluding "no skill exists".

### Fallback: GitHub Deep Search (skill-hunter style)

This is useful when a skill exists in a repo but isn't indexed in skills.sh yet.

1. **If `gh` is available**, search for skill markdown files by keyword:

   ```bash
   gh search code "KEYWORD path:/^./.?(opencode|ai|llm|claude|codex|agents|pi|cursor|factory)\\/skills?\\/.*\\.md$/" --limit 20
   ```

   Tips:
   - Use 2–4 specific keywords (e.g., `playwright e2e`, `nextjs performance`, `pr review`).
   - Prefer results that contain a `SKILL.md` and look actively maintained.

2. **Turn a promising hit into an install:**

   - If you have an `owner/repo` that looks right, list available skills:

     ```bash
     DISABLE_TELEMETRY=1 npx -y skills add owner/repo --list
     ```

   - Then install the specific skill name(s):

     ```bash
     DISABLE_TELEMETRY=1 npx -y skills add owner/repo --skill "<skill-name>" -g --agent codex -y
     ```

3. **If `gh` is not available**, skip this fallback and:
   - Try broader/synonym queries in `npx skills find ...`, or
   - Browse categories on https://skills.sh/ and install from a repo directly, or
   - Proceed without a skill (see next section).

### Still Nothing Found

If there still isn't a good match:

1. Acknowledge that no existing skill was found
2. Offer to help with the task directly using your general capabilities
3. Suggest the user could create their own skill with `npx skills init`

Example:

```
I searched for skills related to "xyz" but didn't find any matches.
I can still help you with this task directly! Would you like me to proceed?

If this is something you do often, you could create your own skill:
npx skills init my-xyz-skill
```
