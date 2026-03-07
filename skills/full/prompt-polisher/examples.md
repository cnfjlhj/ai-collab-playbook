# Prompt Polisher Examples

Real-world before/after transformations showing how the skill processes messy input into polished prompts.

---

## Example 1: Voice Transcription - File Processing Task

### Input (Voice Transcription)

```
okay so um I need to like build something that uh watches a folder and when
new files come in it should like process them somehow maybe convert PDFs to
text or something and then uh save the results somewhere probably a database
but I'm not sure which one yet you know
```

### Gap-Fill Questions

```
Before I polish this prompt, I need to clarify a few things:

1. For PDF processing, do you want OCR support for scanned documents,
   or just text extraction from digital PDFs?

2. Should the processed text be stored with metadata (filename, date,
   page count) or just the raw text content?

3. Which Claude model are you using? (Opus 4.5 / Sonnet 4.5)
```

### User Response

```
Just text extraction, with metadata, Opus 4.5
```

### Polished Prompt (Opus 4.5 Optimized)

```xml
<context>
I need a file monitoring system that automatically processes new PDF documents
and stores the extracted content in a database for later retrieval and search.
</context>

<task>
Build a Python script that:
1. Watches a specified folder for new PDF files
2. Extracts text content from digital PDFs (no OCR needed)
3. Stores results in SQLite with metadata
</task>

<requirements>
- Use watchdog for file monitoring
- Use PyPDF2 or pdfplumber for text extraction
- SQLite database with fields: filename, extracted_text, page_count,
  file_size, processed_date
- Handle errors gracefully (corrupted PDFs, permission issues)
- Keep the solution simple and focused on these requirements only
</requirements>

<success_criteria>
- Script runs continuously, monitoring the folder
- New PDFs are processed within seconds of appearing
- Extracted text and metadata are queryable in SQLite
- Already-processed files are skipped on restart
</success_criteria>
```

---

## Example 2: Voice Transcription - API Integration

### Input (Voice Transcription)

```
so I've got this like API right and I need to basically um connect it to our
frontend but the thing is it's got rate limiting and uh we need to handle
that somehow and also like cache the responses because we're making the same
calls over and over which is dumb you know and oh yeah it needs to work with
our existing React app
```

### Gap-Fill Questions

```
Before I polish this prompt, I need to clarify:

1. What's the rate limit on the API (requests per minute/hour)?
2. How long should cached responses remain valid?
3. Is this a REST API or GraphQL?
4. Which Claude model are you using? (Opus 4.5 / Sonnet 4.5)
```

### User Response

```
100 requests per minute, cache for 5 minutes, REST API, Sonnet 4.5
```

### Polished Prompt (Sonnet 4.5 Optimized)

```xml
<context>
Our React frontend makes repeated calls to an external REST API that has
rate limiting (100 req/min). We need an integration layer that handles
rate limiting and caches responses to reduce redundant calls.
</context>

<task>
Create an API integration service for our React app with rate limiting
and caching.
</task>

<requirements>
- Implement request queue that respects 100 requests/minute limit
- Cache responses for 5 minutes using an appropriate caching strategy
- Integrate with existing React app (provide hooks or context)
- Handle rate limit errors gracefully with retry logic
</requirements>

<success_criteria>
- No rate limit errors reach the frontend
- Cached responses are served instantly for repeated calls
- Cache invalidates correctly after 5 minutes
- Easy to use from React components (useApi hook or similar)
</success_criteria>

<approach>
Complete this in these steps:
1. First, create the caching layer with TTL support
2. Then, implement the rate limiter with request queuing
3. Next, build the API client that uses both
4. Finally, create React hooks for easy consumption

Report progress after each step.
</approach>
```

---

## Example 3: Document Dump - Feature Request

### Input (Rough Notes)

```
feature: dark mode

users have been asking for this forever
need to add toggle in settings
should remember preference
also need to update all the components to support it
maybe use CSS variables?
don't break existing light theme
needs to work on mobile too
```

### Gap-Fill Questions

```
Before I polish this prompt, I need to clarify:

1. Should dark mode follow system preference by default, or start with
   a manual toggle only?
2. Are there specific brand colors that must be used for dark mode, or
   should I derive them from the light theme?
3. Which Claude model are you using? (Opus 4.5 / Sonnet 4.5)
```

### User Response

```
Follow system preference with manual override, derive from light theme, Opus 4.5
```

### Polished Prompt (Opus 4.5 Optimized)

```xml
<context>
Users have requested dark mode support. The app currently has a light theme
only. This needs to be a user-facing feature with a toggle in settings.
</context>

<task>
Add dark mode support to the application with a settings toggle.
</task>

<requirements>
- Default to system preference (prefers-color-scheme)
- Allow manual override via toggle in settings
- Persist user preference in localStorage
- Use CSS custom properties for theme colors
- Derive dark theme colors from existing light theme
- Preserve all existing light theme functionality
- Support mobile responsive layouts
- Keep implementation simple - avoid over-engineering
</requirements>

<success_criteria>
- Toggle appears in settings and works correctly
- Theme persists across sessions
- All existing components render correctly in both themes
- System preference is respected until user overrides
- No visual regressions in light mode
</success_criteria>
```

---

## Example 4: Stream of Consciousness - Debugging

### Input (Stream of Consciousness)

```
ugh so there's this bug where like when users log in sometimes it works and
sometimes it doesn't and I can't figure out what's different between the
times it works and doesn't work and the error message is useless it just
says "authentication failed" and I've checked the password hashing and that
seems fine and the database connection is fine too I think maybe it's a
race condition or something with the session but I'm not sure where to even
start looking
```

### Gap-Fill Questions

```
Before I polish this prompt, I need to clarify:

1. What authentication method are you using (JWT, sessions, OAuth)?
2. Is this happening in development, production, or both?
3. Do you have access to server logs from failed attempts?
4. Which Claude model are you using? (Opus 4.5 / Sonnet 4.5)
```

### User Response

```
JWT tokens, production only, yes I have logs, Opus 4.5
```

### Polished Prompt (Opus 4.5 Optimized)

```xml
<context>
Intermittent login failures in production with JWT authentication. Error
message is generic ("authentication failed"). Password hashing and database
connections appear functional. Suspected race condition with session/token
handling. Server logs are available.
</context>

<task>
Diagnose the root cause of intermittent login failures.
</task>

<requirements>
- Focus investigation on JWT token generation and validation
- Evaluate for race conditions in the authentication flow
- Review server logs for patterns in failed vs successful attempts
- Consider timing-related issues (token expiry, clock skew)
- Keep analysis focused - don't refactor unrelated code
</requirements>

<success_criteria>
- Identify the specific cause of intermittent failures
- Provide evidence from logs or code that confirms the diagnosis
- Propose a targeted fix for the identified issue
</success_criteria>

<approach>
Build an investigation plan first:
1. What specific code paths handle login?
2. Where could race conditions occur?
3. What patterns exist in the logs?

Present findings before proposing solutions.
</approach>
```

---

## Example 5: Simple Input - Minimal Polish

### Input

```
add input validation to the email field in signup form
```

### Assessment

This input is already fairly clear. Minimal polish needed.

### Gap-Fill Questions

```
Quick clarification:

1. Should validation happen on blur, on submit, or real-time as user types?
2. Which Claude model are you using? (Opus 4.5 / Sonnet 4.5)
```

### User Response

```
On blur, Sonnet
```

### Polished Prompt (Streamlined)

```
Add email validation to the signup form's email field. Validate on blur
(when the field loses focus). Show an inline error message for invalid
emails. Use a standard email regex pattern.
```

---

## Example 6: Multi-Document Input

### Input

```
I've uploaded three documents:
- product-requirements.pdf
- technical-spec.md
- competitor-analysis.xlsx

basically I need you to like synthesize these and figure out what we should
actually build for the MVP you know like what's the minimum we can ship that
still beats the competition
```

### Gap-Fill Questions

```
Before I polish this prompt, I need to clarify:

1. What's the target timeline for this MVP?
2. Are there any hard technical constraints (specific tech stack,
   infrastructure limitations)?
3. Which Claude model are you using? (Opus 4.5 / Sonnet 4.5)
```

### User Response

```
3 months, we use React/Node/PostgreSQL, Opus 4.5
```

### Polished Prompt (Opus 4.5 Optimized)

```xml
<context>
Three reference documents have been uploaded:
- product-requirements.pdf: Full product vision and user needs
- technical-spec.md: Technical architecture and constraints
- competitor-analysis.xlsx: Competitive landscape and feature comparison

Goal is to define an MVP scope that's achievable in 3 months using
React/Node/PostgreSQL stack.
</context>

<task>
Synthesize the uploaded documents to recommend MVP scope.
</task>

<requirements>
- Identify features that provide competitive differentiation
- Prioritize based on user value vs implementation effort
- Stay within React/Node/PostgreSQL tech stack
- Scope must be achievable in 3 months
- Keep recommendations focused - avoid scope creep
</requirements>

<success_criteria>
- Clear list of MVP features with prioritization rationale
- Identification of what to explicitly exclude (and why)
- Competitive positioning: how MVP beats alternatives
- Realistic assessment of 3-month feasibility
</success_criteria>

<approach>
Consider each document's perspective, then synthesize:
1. What do users need most? (from requirements)
2. What's technically feasible? (from spec)
3. What differentiates us? (from competitor analysis)

Present a draft feature list for discussion before finalizing.
</approach>
```

---

## Pattern Recognition

| Input Type | Key Cleanup | Common Gaps | Output Style |
|------------|-------------|-------------|--------------|
| Voice transcription | Filler words, self-corrections | Technical specifics, model choice | Full XML structure |
| Rough notes | Bullet normalization, flow | Success criteria, constraints | Full XML structure |
| Stream of consciousness | Sentence structure, focus | Diagnostic info, environment | Investigation-focused |
| Simple requests | Minimal cleanup | Validation timing, edge cases | Streamlined |
| Multi-document | Reference organization | Timeline, constraints | Synthesis-focused |
