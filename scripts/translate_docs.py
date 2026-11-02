"""Translate the documentation's English pages into French, German and Spanish.

Each English page of "Appshare Documentation" (index.md, macos/install.md...)
gets a translation next to it (index.fr.md, index.de.md, index.es.md). Only
the pages changed since their last translation are sent: .translations.json
keeps, for each page and language, the SHA-256 of the English text it was
translated from. Run by `make translate` (or `make docs`, which also uploads).

Needs an Anthropic credential: ANTHROPIC_API_KEY, or an `ant auth login`
profile.
"""

import hashlib
import json
import pathlib
import sys

import anthropic

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "Appshare Documentation"
STATE = ROOT / ".translations.json"
LANGUAGES = {"fr": "French", "de": "German", "es": "Spanish"}
MODEL = "claude-opus-5-5"

SYSTEM = """You translate the documentation of Appshare, a service that publishes media and documents on a customer's own website, from English into {language}.

Return only the translated Markdown page, nothing before or after it.

Keep exactly as they are:
- the Markdown structure: headings and their levels, lists, tables and their alignment, <br /> tags, blank lines
- every URL, link target and image address
- code blocks and inline code
- product and plan names: Appshare, Pro, Business, DemoApp, MauiApp, Stripe, Postman, macOS, Windows
- prices and numbers

Translate the link texts, the table cells and image alternative texts. Write natural, friendly product documentation, addressing the reader the way software documentation usually does in {language}."""


def english_pages():
    """The English pages: every .md file that isn't a translation (index.fr.md)."""
    return sorted(
        path for path in DOCS.rglob("*.md")
        if not any(path.name.endswith(f".{code}.md") for code in LANGUAGES)
    )


def translation_path(page, code):
    return page.with_name(f"{page.stem}.{code}.md")


def translate(client, text, language):
    """The page translated: streamed (long pages), refusals rerun on the
    recommended fallback model by the API itself."""
    with client.beta.messages.stream(
        model=MODEL,
        max_tokens=64000,
        output_config={"effort": "low"},
        betas=["server-side-fallback-2026-07-01"],
        fallbacks="default",
        system=SYSTEM.format(language=language),
        messages=[{"role": "user", "content": text}],
    ) as stream:
        message = stream.get_final_message()
    if message.stop_reason == "refusal":
        raise RuntimeError(f"the translation into {language} was declined")
    if message.stop_reason == "max_tokens":
        raise RuntimeError(f"the translation into {language} was cut off")
    return "".join(block.text for block in message.content if block.type == "text").strip() + "\n"


def main():
    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    client = anthropic.Anthropic()
    done = 0
    for page in english_pages():
        key = str(page.relative_to(DOCS))
        text = page.read_text()
        digest = hashlib.sha256(text.encode()).hexdigest()
        for code, language in LANGUAGES.items():
            target = translation_path(page, code)
            if state.get(key, {}).get(code) == digest and target.exists():
                continue
            print(f"{key} -> {target.name}", flush=True)
            try:
                target.write_text(translate(client, text, language))
            except (anthropic.APIError, RuntimeError) as error:
                print(f"  failed: {error}", file=sys.stderr)
                continue
            state.setdefault(key, {})[code] = digest
            STATE.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")
            done += 1
    print(f"{done} translations written" if done else "Every translation is up to date")


if __name__ == "__main__":
    main()
