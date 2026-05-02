# UI Modernization Plan — 2026-05-02

**Status**: In progress · Branch: `feat/ui-modernization`

## Goal

Polish the bare Streamlit UI into a modern, visually intentional web app. All changes use only Streamlit built-ins and custom CSS via `st.markdown(unsafe_allow_html=True)`. Zero external frontend dependencies.

## Changes

### 1. Centered card layout ✅ Done

Wrap the main content area in a centered column using `st.columns([1, 3, 1])` so the input area, character counter, humanize button, and output are all centered with generous side margins on wide screens. Header stays full-width.

- **Done**: `app.py` lines 181-226.

### 2. Gradient header bar ❌ Abandoned

Custom dark header with gold accent clashed with Streamlit's light theme. Since Streamlit allows users to switch between light and dark themes, a fixed-color header can't work for both. Reverted to native `st.title` + `st.caption` which adapt to the active theme automatically.

### 3. Polished sidebar ⏸️ On hold

The sidebar already houses settings — make it feel curated rather than default. Add bolder section headers, `st.divider()` between logical groups, and a small status indicator showing the active model and strength.

- **Implementation**: Custom CSS targeting `.stSidebar` elements. Group settings into sections with dividers. Add a compact "Active config" summary badge at the bottom.
- **Details**:
  - Section headers in a bolder font, slightly larger
  - Divider between model selection, rewrite strength, and checkbox options
  - A small colored badge showing current model + strength (e.g., "V4 Flash · Medium")

### 4. Character count progress bar ⏸️ On hold

Replace the current colored text (`:gray[{count:,} / {max:,} characters]`) with a horizontal bar that fills as the user types. Color transitions based on usage: green → yellow → red as the limit approaches.

- **Implementation**: Two nested `st.markdown` divs — an outer track and an inner fill bar whose width is set to `{percentage}%`. Color logic in Python: `<50%` green, `50-80%` yellow, `>80%` red. Center the count number over or next to the bar.
- **States**: Empty (0 chars, no bar), normal (green fill), warning (yellow at 50%), danger (red at 80%), and over-limit (full red, pulsing or error treatment).

### 5. One-click copy button ⏸️ On hold

After the model returns rewritten text, show a copy button next to the output text area. One click copies the full result to the clipboard.

- **Implementation**: Use `st.markdown` with an HTML `<button>` and a small inline JavaScript snippet that calls `navigator.clipboard.writeText()`. A Streamlit component is overkill — a `<script>` block in the page and a styled button element is enough.
- **Behavior**: Brief visual feedback on click (e.g., button text changes to "Copied!" for 2 seconds, then reverts).

## Non-goals

- Tab/compare views between original and rewritten text
- Dark/light theme toggle (Streamlit's built-in theme is sufficient)
- External CSS frameworks or component libraries
- Responsive breakpoints beyond the centered card (Streamlit handles mobile adequately)

## Implementation order

**Done**: 1 (centered card layout)

**Abandoned**: 2 (custom header — clashes with theme switching)

**On hold**: 3 → 4 → 5 (sidebar polish, character bar, copy button)
