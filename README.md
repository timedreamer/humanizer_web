# Humanizer

Rewrite AI text to sound human. Based on the [Humanizer](https://github.com/blader/humanizer) writing principles.

Built by **Ji Huang**.

## How it works

The app sends your text to the DeepSeek API with a detailed system prompt covering 29 AI writing patterns — from inflated vocabulary and emoji overuse to formulaic structures and soulless tone. The model rewrites the text, then returns a natural, human-sounding version.

## API configuration

The app calls the [DeepSeek API](https://api-docs.deepseek.com/) with the model selected in the sidebar (`deepseek-v4-flash` or `deepseek-v4-pro`).

**Thinking mode is disabled** (`thinking.type = "disabled"`). DeepSeek's thinking mode runs an internal chain-of-thought before producing the final output, which consumes extra reasoning tokens. Humanization is a straightforward rewrite task — it benefits from clean, direct output, not extended reasoning. Disabling it avoids paying for reasoning tokens that add no value to the result.

**Prompt caching is built into the request structure.** The system prompt (~4K tokens, covering 29 AI writing patterns) is a static constant placed at index 0 of every request. The user message (settings + input text) follows after. DeepSeek automatically caches repeated prefixes, so the system prompt hits cache on every call. Only the dynamic user text at the end misses the cache, keeping costs low across repeated uses.

## Local development

```bash
source .venv/bin/activate
uv pip install -r requirements.txt
streamlit run app.py
```

## Configuration

Create `.streamlit/secrets.toml`:

```toml
APP_PASSWORD = "your-password"
DEEPSEEK_API_KEY = "sk-your-api-key"
```

## Deploy to Streamlit Community Cloud

1. Push this repo to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in.
3. Click **New app**, then select this repository, branch (`main`), and main file path (`app.py`).
4. In the app dashboard, go to **Settings → Secrets** and add:

```toml
APP_PASSWORD = "your-password"
DEEPSEEK_API_KEY = "sk-your-api-key"
```

5. Click **Save** — the app redeploys with your secrets. It's now live at `https://<your-app>.streamlit.app`.
