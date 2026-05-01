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
        st.text_area(
            "Humanized output",
            value=st.session_state["humanized_output"],
            height=400,
        )


if __name__ == "__main__":
    main()
