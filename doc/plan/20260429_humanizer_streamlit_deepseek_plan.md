# Humanizer Web App Plan

## Goal

Build a private, Python-only web app for rewriting pasted text to sound more natural and less AI-generated, inspired by the `blader/humanizer` skill.

The first version should be:

- Simple to build and maintain
- Written in Python
- Hosted for free
- Protected by a password
- Safe from accidental public API-key exposure
- Easy to hand off to Codex CLI, Gemini CLI, Claude Code, or another coding agent

## Recommended Stack

| Layer | Choice |
|---|---|
| Web framework | Streamlit |
| Hosting | Streamlit Community Cloud |
| LLM provider | DeepSeek API first; OpenAI/Anthropic optional later |
| Authentication | Shared password stored in Streamlit secrets |
| Repository | GitHub |
| Main language | Python |
| Frontend | Streamlit-generated UI; no JavaScript required |

## Why This Stack

Streamlit is the simplest option because the entire app can be implemented in a single Python file. It avoids the need for React, Next.js, JavaScript, TypeScript, separate frontend/backend code, or serverless routing.

Streamlit Community Cloud is suitable because the app will not host a model locally. It will only call an external LLM API, so CPU and memory needs should be low.

## Core User Flow

1. User opens the Streamlit app URL.
2. User enters a shared password.
3. If the password is correct, the app shows the humanizer interface.
4. User pastes text into a large text area.
5. User optionally selects rewrite settings.
6. User clicks **Humanize**.
7. The app sends the text and prompt to the LLM API.
8. The rewritten output appears in the app.
9. User copies the output manually.

## Minimum Repository Structure

```text
humanizer-web/
  app.py
  requirements.txt
  .gitignore
  README.md
  .streamlit/
    secrets.example.toml
```

Do not commit a real `.streamlit/secrets.toml` file. Commit only `secrets.example.toml` as a template.

## Required Secrets

Store these in Streamlit Community Cloud secrets, not in GitHub.

```toml
APP_PASSWORD = "replace-with-a-strong-password"
DEEPSEEK_API_KEY = "replace-with-deepseek-api-key"
```

Optional future provider support:

```toml
OPENAI_API_KEY = "replace-with-openai-api-key"
ANTHROPIC_API_KEY = "replace-with-anthropic-api-key"
```

## DeepSeek API Notes

DeepSeek provides an OpenAI-compatible API format. For the first version, use the official OpenAI Python SDK with DeepSeek's base URL.

Use:

```text
base_url = "https://api.deepseek.com"
```

Recommended default model:

```text
deepseek-v4-flash
```

Optional stronger model:

```text
deepseek-v4-pro
```

Avoid using these legacy names for a new app:

```text
deepseek-chat
deepseek-reasoner
```

DeepSeek's official docs say `deepseek-chat` and `deepseek-reasoner` are compatibility names scheduled for deprecation on 2026-07-24.

## Local Secrets Template

Create this file for the repository template:

```toml
# .streamlit/secrets.example.toml

APP_PASSWORD = "replace-with-local-password"
DEEPSEEK_API_KEY = "replace-with-deepseek-api-key"
```

For local testing, copy it to:

```text
.streamlit/secrets.toml
```

Then replace the placeholder values. The real `secrets.toml` file must stay local and must not be committed.

## `.gitignore`

```gitignore
.streamlit/secrets.toml
.env
__pycache__/
*.pyc
.DS_Store
```

## `requirements.txt`

For the DeepSeek first version, still use the `openai` Python package because DeepSeek supports an OpenAI-compatible API.

```text
streamlit
openai
```

Optional later version with multiple providers:

```text
streamlit
openai
anthropic
```

## First-Version Features

### Must Have

- Password gate
- Text input area
- Humanize button
- Output area
- Character count
- Maximum character limit
- LLM API call
- Prompt designed for natural rewriting
- Error handling for missing secrets, wrong password, empty input, and overly long input

### Should Have

- Sidebar settings
- Model selector
- Tone selector
- Preserve Markdown option
- More concise option
- Copy-friendly output text area

### Not Needed in Version 1

- User accounts
- OAuth login
- Database
- Per-user quotas
- Payment system
- File upload
- Request history
- React/Next.js
- Netlify/Vercel
- Local model hosting

## Application Logic and UI Flow

### Step A: Authentication Gate

On first load, check `st.session_state` for an `authenticated` flag. If not present or False, render:

- App title
- App caption
- Password input

If the password matches `st.secrets["APP_PASSWORD"]`, set `st.session_state.authenticated = True` and trigger `st.rerun()`.

### Step B: Main Interface After Login

If authenticated, render:

- Sidebar settings
- Large paste input
- Character counter
- Humanize button (disabled if input is empty or over the character limit)
- Loading spinner during the API call
- Output area with a native copy-to-clipboard button (`st.code`)

### Step C: DeepSeek API Call

Use the OpenAI Python SDK with DeepSeek's OpenAI-compatible endpoint:

```python
from openai import OpenAI

client = OpenAI(
    api_key=st.secrets["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com",
)
```

Use `client.chat.completions.create(...)`, not the OpenAI Responses API, because DeepSeek's OpenAI-compatible examples use the chat completions format.

### Step D: Error Handling

Wrap the model call in `try/except` and show user-friendly Streamlit errors for:

- Missing secrets
- API errors
- Network or timeout errors

## Suggested UI

### Main Page

Title:

```text
Humanizer
```

Subtitle:

```text
Paste text and rewrite it to sound more natural while preserving the original meaning.
```

Elements:

1. Password input
2. Text area for input
3. Character counter
4. Humanize button
5. Output text area
6. Warning or error messages

### Sidebar

Settings:

- Model
  - `gpt-4.1-mini` or another low-cost default model
  - optionally `gpt-4.1` or newer stronger model
- Rewrite strength
  - Light
  - Medium
  - Strong
- Output style
  - Natural
  - Concise
  - Professional
  - Casual
- Preserve Markdown
  - True by default
- Preserve citations
  - True by default

## Password Gate Logic

### Step A: Authentication Gate

The first rendered UI should be minimal:

- App title
- Short description
- Password input box

Do not show the text input or model settings until the password is correct.

Implementation requirements:

- Use `st.secrets["APP_PASSWORD"]`.
- Use `st.session_state` to track if the user is `authenticated`.
- If not authenticated:
    - Show password input: `st.text_input(..., type="password", on_change=check_password)`.
    - If the password is missing from secrets, show `st.error`.
    - `st.stop()` to prevent rendering the rest of the app.
- This approach hides the login form once the user is successfully authenticated.

This is not enterprise-grade authentication, but it is acceptable for a personal tool or a few trusted users.


## LLM Prompt

Use this as the initial system prompt.

```text
You are a careful rewriting assistant.

Rewrite the user's text to sound natural, human-written, and less AI-generated.

Preserve:
- The original meaning
- Technical accuracy
- Markdown structure
- Citations and references
- Code blocks
- Equations
- Names, dates, numbers, and domain-specific terms

Improve:
- Overly polished AI phrasing
- Inflated or promotional language
- Generic transitions
- Repetitive sentence rhythm
- Excessive em dashes
- Vague claims
- Awkward passive voice
- Filler phrases
- Unnatural "rule of three" phrasing

Do not:
- Add new facts
- Remove important details
- Invent citations
- Change code
- Change quoted text unless necessary
- Explain your changes

Return only the rewritten text.
```

## Rewrite Strength Behavior

Use a setting to modify the prompt.

### Light

```text
Make minimal edits. Keep the user's wording and structure mostly intact. Only smooth obviously unnatural or AI-like phrasing.
```

### Medium

```text
Improve flow, sentence rhythm, and naturalness while preserving the structure and all meaning.
```

### Strong

```text
Rewrite more freely for a natural human style, but preserve all factual meaning, technical details, citations, and formatting.
```

## Model Name Decision

Do not use `deepseek-chat` for a new implementation unless DeepSeek changes its docs again.

Use:

```text
deepseek-v4-flash
```

as the default model.

Use:

```text
deepseek-v4-pro
```

as the optional stronger model.

Reason: DeepSeek's current docs list `deepseek-chat` and `deepseek-reasoner` as compatibility names and indicate they will be deprecated. New code should use the current `deepseek-v4-*` model names.

## Suggested `app.py` Skeleton

```python
import streamlit as st
from openai import OpenAI

APP_TITLE = "Humanizer"
MAX_CHARS = 12000
DEEPSEEK_BASE_URL = "https://api.deepseek.com"

SYSTEM_PROMPT = '''
You are a careful rewriting assistant.

Rewrite the user's text to sound natural, human-written, and less AI-generated.

Preserve:
- The original meaning
- Technical accuracy
- Markdown structure
- Citations and references
- Code blocks
- Equations
- Names, dates, numbers, and domain-specific terms

Improve:
- Overly polished AI phrasing
- Inflated or promotional language
- Generic transitions
- Repetitive sentence rhythm
- Excessive em dashes
- Vague claims
- Awkward passive voice
- Filler phrases
- Unnatural "rule of three" phrasing

Do not:
- Add new facts
- Remove important details
- Invent citations
- Change code
- Change quoted text unless necessary
- Explain your changes

Return only the rewritten text.
'''.strip()


def get_secret(name: str) -> str:
    value = st.secrets.get(name)
    if not value:
        st.error(f"Missing required secret: {name}")
        st.stop()
    return value


def check_password():
    """Verifies the password and updates session state."""
    expected = get_secret("APP_PASSWORD")
    if st.session_state["password_input"] == expected:
        st.session_state["authenticated"] = True
        del st.session_state["password_input"]
    else:
        st.error("Incorrect password.")
        st.session_state["authenticated"] = False


def require_password() -> None:
    """Renders the login UI if not authenticated."""
    if st.session_state.get("authenticated"):
        return

    st.text_input(
        "Password",
        type="password",
        on_change=check_password,
        key="password_input",
    )
    st.info("Enter the password to use this app.")
    st.stop()


def build_user_prompt(
    text: str,
    rewrite_strength: str,
    output_style: str,
    preserve_markdown: bool,
    make_concise: bool,
) -> str:
    instructions = [
        f"Rewrite strength: {rewrite_strength}.",
        f"Output style: {output_style}.",
    ]

    if preserve_markdown:
        instructions.append("Preserve the original Markdown structure as much as possible.")
    else:
        instructions.append("Markdown preservation is not required.")

    if make_concise:
        instructions.append("Make the output more concise while preserving meaning.")

    instructions.append("Text to rewrite:")
    instructions.append(text)

    return "\n\n".join(instructions)


@st.cache_resource
def get_client() -> OpenAI:
    api_key = get_secret("DEEPSEEK_API_KEY")
    return OpenAI(api_key=api_key, base_url=DEEPSEEK_BASE_URL)


def humanize_text(
    text: str,
    model: str,
    rewrite_strength: str,
    output_style: str,
    preserve_markdown: bool,
    make_concise: bool,
) -> str:
    client = get_client()

    user_prompt = build_user_prompt(
        text=text,
        rewrite_strength=rewrite_strength,
        output_style=output_style,
        preserve_markdown=preserve_markdown,
        make_concise=make_concise,
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        stream=False,
        extra_body={"thinking": {"type": "disabled"}},
    )

    return response.choices[0].message.content.strip()


def main() -> None:
    st.set_page_config(page_title=APP_TITLE, page_icon="✍️", layout="wide")

    st.title(APP_TITLE)
    st.caption("Rewrite pasted text to sound more natural while preserving meaning.")

    require_password()

    with st.sidebar:
        st.header("Settings")
        
        if st.button("Logout"):
            st.session_state["authenticated"] = False
            st.rerun()

        model = st.selectbox(
            "Model",
            [
                "deepseek-v4-flash",
                "deepseek-v4-pro",
            ],
            index=0,
        )

        rewrite_strength = st.radio(
            "Rewrite strength",
            ["Light", "Medium", "Strong"],
            index=1,
        )

        output_style = st.selectbox(
            "Output style",
            ["Natural", "Concise", "Professional", "Casual"],
            index=0,
        )

        preserve_markdown = st.checkbox("Preserve Markdown", value=True)
        make_concise = st.checkbox("Make more concise", value=False)

    input_text = st.text_area(
        "Paste text to humanize",
        height=300,
        placeholder="Paste your text here...",
    )

    char_count = len(input_text)
    is_over_limit = char_count > MAX_CHARS
    is_empty = not input_text.strip()

    color = "red" if is_over_limit else "gray"
    st.markdown(f":{color}[{char_count:,} / {MAX_CHARS:,} characters]")

    if is_over_limit:
        st.error(f"Input is too long. Please keep it under {MAX_CHARS:,} characters.")

    if st.button(
        "Humanize",
        type="primary",
        disabled=is_over_limit or is_empty,
    ):
        with st.spinner("Rewriting..."):
            try:
                output = humanize_text(
                    text=input_text,
                    model=model,
                    rewrite_strength=rewrite_strength,
                    output_style=output_style,
                    preserve_markdown=preserve_markdown,
                    make_concise=make_concise,
                )
                st.session_state["humanized_output"] = output
            except Exception as exc:
                st.error(f"Failed to rewrite text: {exc}")

    if "humanized_output" in st.session_state:
        st.subheader("Humanized output")
        st.code(st.session_state["humanized_output"], language=None)


if __name__ == "__main__":
    main()
```

## Streamlit Community Cloud Deployment Steps

1. Create a GitHub repository, for example:

   ```text
   humanizer-web
   ```

2. Add and commit these files:

   ```text
   app.py
   requirements.txt
   .gitignore
   README.md
   .streamlit/secrets.example.toml
   ```

3. Do not commit this file:

   ```text
   .streamlit/secrets.toml
   ```

4. Push the repository to GitHub.

5. Go to Streamlit Community Cloud.

6. Create a new app from the GitHub repository.

7. Set the main file path:

   ```text
   app.py
   ```

8. Before deploying, open the app's advanced settings or secrets settings and paste:

   ```toml
   APP_PASSWORD = "your-password"
   DEEPSEEK_API_KEY = "your-deepseek-api-key"
   ```

9. Deploy the app.

10. Open the app URL and test:

   - wrong password
   - correct password
   - empty input
   - normal input
   - long input
   - Markdown input
   - text with citations
   - text with code block
   - temporary API failure handling


## Optional DeepSeek Sanity Check

Before deploying, test the API key locally with the OpenAI-compatible client:

```python
from openai import OpenAI

client = OpenAI(
    api_key="your-deepseek-api-key",
    base_url="https://api.deepseek.com",
)

response = client.chat.completions.create(
    model="deepseek-v4-flash",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Reply with one short sentence."},
    ],
    stream=False,
    extra_body={"thinking": {"type": "disabled"}},
)

print(response.choices[0].message.content)
```

Use `thinking` disabled for the humanizer default because the task is a style rewrite and should be fast and inexpensive. If a future mode requires heavier reasoning, add a separate option that uses `deepseek-v4-pro` with thinking enabled.

## Local Development

Create local secrets by copying the template:

```bash
mkdir -p .streamlit
cp .streamlit/secrets.example.toml .streamlit/secrets.toml
```

Then edit `.streamlit/secrets.toml` and replace the placeholder values.

Alternatively, create it manually:

```bash
mkdir -p .streamlit
cat > .streamlit/secrets.toml <<'EOF'
APP_PASSWORD = "local-password"
DEEPSEEK_API_KEY = "your-deepseek-api-key"
EOF
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run app:

```bash
streamlit run app.py
```

Open the local URL shown by Streamlit.

## Security Notes

This is a lightweight personal app, not enterprise authentication.

The password gate is acceptable for:

- Personal use
- A few trusted users
- Low-risk text rewriting

It is not enough for:

- Paid public product
- Sensitive multi-user document processing
- Strict per-user access control
- Detailed quota enforcement

Minimum safety controls:

- Store API key only in secrets
- Store password only in secrets
- Add a max character limit
- Do not log full user text
- Do not commit `.streamlit/secrets.toml`
- Rotate the password if shared too widely

## Cost Control

Start with:

```text
MAX_CHARS = 12000
default model = deepseek-v4-flash
```

Possible later controls:

- Lower max character limit
- Add daily request counter
- Add per-session usage count
- Add cooldown between requests
- Add approximate token/cost estimate before submission

For Version 1, a max character limit and password gate are probably enough.

## Future Improvements

### Useful Next Features

- **Streaming output**: Implement `stream=True` once confirmed compatible with the DeepSeek API to improve perceived performance.
- Before/after diff: Show the changes made by the AI.
- OpenAI/Anthropic provider option: Add support for other LLM backends.
- User-specific passwords: Move away from a single shared password.
- Basic request count: Track usage per session or globally.
- Export output as Markdown: Download the result as a `.md` file.
- Multiple prompt presets: Save and load different custom instructions.
- Batch mode: Process several paragraphs or documents at once.
- Local prompt editor: Allow trusted users to tweak the system prompt.

### More Advanced Later

- Real login with Google OAuth
- Database-backed quotas
- Admin dashboard
- Usage analytics
- API endpoint
- Browser extension
- Chrome side panel
- VS Code/Cursor/Codex integration

## Decision Summary

Use:

```text
Streamlit + Streamlit Community Cloud + shared password + DeepSeek API
```

Do not use, for Version 1:

```text
React
Next.js
Vercel
Netlify
Database
OAuth
Docker
Local model hosting
```

This is the simplest path for a Python-first personal humanizer web app.
