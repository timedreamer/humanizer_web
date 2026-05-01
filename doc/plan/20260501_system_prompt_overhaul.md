# Plan: Overhaul System Prompt Based on Real Humanizer Skill

## Context

The current `SYSTEM_PROMPT` in `app.py` is ~20 lines of generic advice. The real humanizer skill (SKILL.md v2.5.1) defines 29 specific patterns with vocabulary lists, a 6-step process, personality guidelines, and a draft→audit→final output format. The prompt needs to encode this expertise so the DeepSeek model produces genuinely human-sounding output, not just lightly-edited AI text.

Voice Calibration (sample-based matching) is explicitly out of scope for this round.

## Design Decisions

### Prompt storage: new `prompts.py` file
The new system prompt will be ~500+ lines. Storing it in `app.py` would bloat the file to ~700 lines mixing logic and content. A separate `prompts.py` in the project root keeps concerns clean. The prompt is one cohesive document — splitting across multiple files buys nothing.

### Pattern inclusion: all 29, tiered by depth
Not all 29 patterns need equal treatment. High-frequency/high-distinctiveness patterns get full vocabulary lists and examples; simpler patterns get concise descriptions.

### Output format: two modes
- **Default (Show full analysis = OFF):** Model does the full internal process but outputs only the final rewrite. Same clean UX as today.
- **Analysis mode (Show full analysis = ON):** Model outputs Draft → Anti-AI Audit → Final Rewrite → Summary. For power users who want transparency.

### Existing controls: keep all
Rewrite strength, output style, preserve markdown, and make concise all remain meaningful. Add one new checkbox: "Show full analysis."

## System Prompt Structure (7 sections, ~1500 words)

1. **Identity & Core Mission** — You are a rewriting editor removing AI signs
2. **Non-Negotiable Preservation Rules** — meaning, accuracy, citations, code, equations, names/dates/numbers
3. **Content Patterns (1-6)** — undue emphasis, notability padding, -ing analyses, promotional language, vague attributions, formulaic challenges sections. Full trigger word lists for patterns 1 and 4.
4. **Language & Grammar (7-13)** — **Full AI vocabulary list** (crucial, delve, showcase, tapestry, etc.), copula avoidance (serves as→is, boasts→has), negative parallelisms, rule of three, elegant variation, false ranges, passive voice fragments
5. **Style & Formatting (14-19)** — em dash→commas, boldface removal, inline-header lists→prose, title case→sentence case, emojis→plain text, curly quotes→straight quotes
6. **Communication & Filler (20-29)** — chatbot artifacts, knowledge-cutoff disclaimers, sycophantic tone, filler phrases with replacement table, excessive hedging, generic positive conclusions, hyphenated pairs, persuasive tropes, signposting, fragmented headers
7. **Personality, Soul & Process** — 6 personality guidelines (have opinions, vary rhythm, acknowledge complexity, use "I", let mess in, be specific) + 6-step process + final anti-AI audit instruction

### User prompt adaptation
`build_user_prompt()` gets richer strength/style descriptions and passes through the `show_analysis` flag:

- **Light:** Apply corrections conservatively. Fix only obvious AI tells. Preserve original voice.
- **Medium:** Apply corrections moderately. Rewrite common AI patterns while maintaining structure.
- **Strong:** Rewrite freely. Prioritize human voice. Restructure sentences as needed.
- **Natural:** Default human tone with personality guidelines.
- **Concise:** Tighten wordy phrasing, remove redundancy.
- **Professional:** Restrained, measured tone.
- **Casual:** Conversational, contractions, first-person, informal.

## Files to Create/Modify

| File | Action |
|------|--------|
| `prompts.py` | **Create** — SYSTEM_PROMPT constant (~500 lines), STRENGTH_INSTRUCTIONS dict, STYLE_INSTRUCTIONS dict |
| `app.py` | **Modify** — Remove old SYSTEM_PROMPT, add import from prompts.py, update `build_user_prompt()`, add `show_analysis` checkbox to sidebar, update `humanize_text()` signature, update output display area |

## Implementation Steps

1. **Create `prompts.py`** with the comprehensive SYSTEM_PROMPT and instruction dicts
2. **Update `app.py` imports** — remove old SYSTEM_PROMPT, import from prompts.py
3. **Update `build_user_prompt()`** — richer format with strength/style descriptions from dicts, show_analysis flag
4. **Add "Show full analysis" checkbox** to sidebar (default off)
5. **Update `humanize_text()`** — accept `show_analysis` param, pass through
6. **Update output display** — use `st.text_area()` for both modes (simpler and handles markdown better)
7. **Test** — run the app, paste AI-generated text, verify output at each strength level, toggle analysis mode

## Verification

1. Start the app: `.venv/bin/streamlit run app.py`
2. Paste text from `data/text_for_test.txt` and verify humanization at Light/Medium/Strong
3. Toggle "Show full analysis" on and verify draft→audit→final format
4. Test with markdown-heavy text — verify code blocks, headings, links preserved
5. Test edge cases: empty input (button disabled), near-8000-char input
6. Verify each output style produces distinct tonal differences
