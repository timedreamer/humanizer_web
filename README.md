# Humanizer Web App

Rewrite AI text to sound human. Based on the [Humanizer](https://github.com/blader/humanizer) writing principles.

Built by **Ji Huang**.

## Features

- **Model choice** — `deepseek-v4-flash` (fast, affordable) or `deepseek-v4-pro` (highest quality). Thinking mode is disabled — rewriting works better with direct output.
- **Rewrite strength** — Light (fix only obvious AI tells), Medium (balanced corrections), or Strong (full human voice).
- **Preserve Markdown** — Keep headings, lists, code blocks, and formatting intact through the rewrite.
- **Full analysis mode** — For power users: see the draft, an anti-AI audit of remaining tells, and the final version, so you understand what changed and why.
- **Soft password gate** — A password prompt keeps bots away. The password is displayed on the login screen so anyone can get in without asking.
- **Rate limiting** — 30 requests per hour per session to prevent runaway API usage.

## Screenshot

![Humanizer app screenshot](screenshot.png)

## How it works

The app sends your text to the [DeepSeek API](https://api-docs.deepseek.com/) with a detailed system prompt covering 29 AI writing patterns — from inflated vocabulary and emoji overuse to formulaic structures and soulless tone. The model rewrites the text and returns a natural, human-sounding version.

Thinking mode is disabled (`thinking.type = "disabled"`). DeepSeek's reasoning step consumes extra tokens but adds no value for a rewrite task. Prompt caching is automatic — the static system prompt hits cache on every call, so only the user's input text costs tokens.

## Local development

```bash
source .venv/bin/activate
uv pip install -r requirements.txt
streamlit run app.py
```

## Configuration

Create `.streamlit/secrets.toml`:

```toml
APP_PASSWORD = "keepbotaway"
DEEPSEEK_API_KEY = "sk-your-api-key"
```

The password is shown as a hint on the login page — it's a soft gate to keep bots out, not a secret. Pick something short and easy to type.

## Deploy to Streamlit Community Cloud

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in.
3. Click **New app**, then select this repository, branch (`main`), and main file path (`app.py`).
4. In the app dashboard, go to **Settings → Secrets** and add:

```toml
APP_PASSWORD = "keepbotaway"
DEEPSEEK_API_KEY = "sk-your-api-key"
```

5. Click **Save** — the app redeploys with your secrets. It's now live at `https://<your-app>.streamlit.app`.
