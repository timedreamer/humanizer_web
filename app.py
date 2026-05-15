import time

import streamlit as st
from openai import OpenAI

from prompts import SYSTEM_PROMPT, STRENGTH_INSTRUCTIONS

APP_TITLE = "Humanizer"
MAX_CHARS = 8000
MIN_CHARS = 10
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
MAX_REQUESTS_PER_HOUR = 30
RATE_WINDOW_SECONDS = 3600


def get_secret(name: str) -> str:
    value = st.secrets.get(name)
    if not value:
        st.error(f"Missing required secret: {name}")
        st.stop()
    return value


def _count_requests() -> int:
    now = time.time()
    window_start = now - RATE_WINDOW_SECONDS
    return sum(1 for ts in st.session_state.get("request_timestamps", []) if ts > window_start)


def _check_rate_limit() -> bool:
    return _count_requests() < MAX_REQUESTS_PER_HOUR


def _record_request():
    if "request_timestamps" not in st.session_state:
        st.session_state.request_timestamps = []
    st.session_state.request_timestamps.append(time.time())


def remaining_quota() -> int:
    return max(0, MAX_REQUESTS_PER_HOUR - _count_requests())


def check_password():
    expected = get_secret("APP_PASSWORD")
    if st.session_state["password_input"] == expected:
        st.session_state["authenticated"] = True
        del st.session_state["password_input"]
    else:
        st.error("Incorrect password.")
        st.session_state["authenticated"] = False


def require_password() -> None:
    if st.session_state.get("authenticated"):
        return

    st.text_input(
        "Password",
        type="password",
        on_change=check_password,
        key="password_input",
    )
    st.info(f"Password: **{get_secret('APP_PASSWORD')}**")
    st.stop()


def build_user_prompt(
    text: str,
    rewrite_strength: str,
    preserve_markdown: bool,
    show_analysis: bool = False,
) -> str:
    parts: list[str] = [
        f"Rewrite strength: {rewrite_strength}.",
        STRENGTH_INSTRUCTIONS[rewrite_strength],
    ]

    if preserve_markdown:
        parts.append("Preserve the original Markdown structure as much as possible.")
    else:
        parts.append("Markdown preservation is not required.")

    if show_analysis:
        parts.append(
            "Output format: First provide your draft rewrite. Then briefly list "
            "remaining AI tells under 'Anti-AI Audit:' (bullet points). Then provide "
            "the final revised version. Then a brief summary of changes made."
        )
    else:
        parts.append("Return only the final rewritten text. No drafts, notes, or explanations.")

    parts.append("Text to rewrite:")
    parts.append(text)

    return "\n\n".join(parts)


@st.cache_resource
def get_client() -> OpenAI:
    api_key = get_secret("DEEPSEEK_API_KEY")
    return OpenAI(api_key=api_key, base_url=DEEPSEEK_BASE_URL)


def humanize_text(
    text: str,
    model: str,
    rewrite_strength: str,
    preserve_markdown: bool,
    show_analysis: bool = False,
) -> str:
    if not _check_rate_limit():
        st.error(
            f"Rate limit reached ({MAX_REQUESTS_PER_HOUR} requests per hour). "
            "Please wait for the window to reset."
        )
        st.stop()

    client = get_client()

    user_prompt = build_user_prompt(
        text=text,
        rewrite_strength=rewrite_strength,
        preserve_markdown=preserve_markdown,
        show_analysis=show_analysis,
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

    content = response.choices[0].message.content
    _record_request()
    return content.strip() if content else ""


def main() -> None:
    st.set_page_config(page_title=APP_TITLE, page_icon="✍️", layout="wide")

    st.markdown(
        """
        <style>
        .stTextArea textarea { font-size: 18px !important; }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title(APP_TITLE)
    st.caption(
        "By **Ji Huang**. Rewrite AI text to sound human. "
        "Based on the [Humanizer](https://github.com/blader/humanizer) writing principles. "
        "[GitHub](https://github.com/timedreamer/humanizer_web)"
    )

    require_password()

    with st.sidebar:
        st.header("Settings")

        if st.button("Logout"):
            st.session_state["authenticated"] = False
            st.session_state.pop("request_timestamps", None)
            st.rerun()

        st.caption(
            f"Remaining: **{remaining_quota()}/{MAX_REQUESTS_PER_HOUR}** requests this hour"
        )

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

        preserve_markdown = st.checkbox("Preserve Markdown", value=True)
        show_analysis = st.checkbox("Show full analysis", value=False)

    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        input_text = st.text_area(
            "Paste text to humanize",
            height=300,
            placeholder="Paste your text here...",
        )

        char_count = len(input_text)
        is_over_limit = char_count > MAX_CHARS
        is_empty = not input_text.strip()
        is_too_short = 0 < char_count < MIN_CHARS

        color = "red" if (is_over_limit or is_too_short) else "gray"
        st.markdown(f":{color}[{char_count:,} / {MAX_CHARS:,} characters]")

        if is_over_limit:
            st.error(f"Input is too long. Please keep it under {MAX_CHARS:,} characters.")
        elif is_too_short:
            st.warning(f"Input is too short. Please paste at least {MIN_CHARS} characters.")

        if st.button(
            "Humanize",
            type="primary",
            disabled=is_over_limit or is_empty or is_too_short,
        ):
            with st.spinner("Rewriting..."):
                try:
                    output = humanize_text(
                        text=input_text,
                        model=model,
                        rewrite_strength=rewrite_strength,
                        preserve_markdown=preserve_markdown,
                        show_analysis=show_analysis,
                    )
                    st.session_state["humanized_output"] = output
                except Exception as exc:
                    st.error(f"Failed to rewrite text: {exc}")

        if "humanized_output" in st.session_state:
            st.subheader("Humanized output")
            st.text_area(
                "Humanized output",
                value=st.session_state["humanized_output"],
                height=400,
            )


if __name__ == "__main__":
    main()
