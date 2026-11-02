"""Translate the documentation's English pages into French, German and Spanish.

Each English page of "Appshare Documentation" (index.md, macos/install.md...)
gets a translation next to it (index.fr.md, index.de.md, index.es.md). Only
the pages changed since their last translation are sent: .translations.json
keeps, for each page and language, the SHA-256 of the English text it was
translated from. Run by `make translate` (or `make docs`, which also uploads).

Translated by Azure AI Translator (REST API v3, HTML mode). The service
translates text, not Markdown, so each line is sent on its own (the page's
structure can't move) and what must not change is kept out of the
translation: code blocks, table separators and <br /> lines aren't sent;
inside a line, link and image addresses, inline code and table pipes are
marked notranslate; bold and italic go as <b>/<i> and come back as Markdown.

Needs AZURE_TRANSLATOR_KEY and AZURE_TRANSLATOR_REGION (the Translator
resource's key and location, e.g. francecentral).
"""

import hashlib
import html
import json
import os
import pathlib
import re
import sys
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
DOCS = ROOT / "Appshare Documentation"
STATE = ROOT / ".translations.json"
LANGUAGES = ["fr", "de", "es"]
ENDPOINT = os.environ.get("AZURE_TRANSLATOR_ENDPOINT", "https://api.cognitive.microsofttranslator.com")

# A line's Markdown prefix, kept as is: heading, list item, quote
PREFIX = re.compile(r"^(\s*(?:#{1,6}\s+|[-*+]\s+|\d+\.\s+|>\s*)?)(.*)$")
# The lines not sent at all
TABLE_SEPARATOR = re.compile(r"^\s*\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)*\|?\s*$")
ONLY_TAGS = re.compile(r"^\s*(<[^>]+>\s*)+$")
# Inside a line: what is protected or converted, in this order
INLINE = re.compile(
    r"(?P<code>`[^`]+`)"
    r"|(?P<image>!\[[^\]]*\]\([^)]*\))"
    r"|(?P<link>\[(?P<text>[^\]]+)\]\((?P<url>[^)]+)\))"
    r"|(?P<strong3>\*\*\*(?P<s3>.+?)\*\*\*)"
    r"|(?P<strong2>\*\*(?P<s2>.+?)\*\*)"
    r"|(?P<em>(?<![\w*])\*(?P<e1>[^*\s][^*]*?)\*(?![\w*]))"
    r"|(?P<tag><[^>]+>)"
    r"|(?P<pipe>\|)"
)


def keep(text):
    """Text the translation must leave alone"""
    return f'<span class="notranslate">{html.escape(text, quote=False)}</span>'


def to_html(text, urls):
    """A line's text as HTML for the translator; the links' addresses go to
    `urls` and their tags carry only their number"""
    out, last = [], 0
    for match in INLINE.finditer(text):
        out.append(html.escape(text[last:match.start()], quote=False))
        last = match.end()
        if match["code"] or match["image"] or match["tag"] or match["pipe"]:
            out.append(keep(match.group(0)))
        elif match["link"]:
            urls.append(match["url"])
            out.append(f'<a href="{len(urls) - 1}">{to_html(match["text"], urls)}</a>')
        elif match["strong3"]:
            out.append(f"<b><i>{to_html(match['s3'], urls)}</i></b>")
        elif match["strong2"]:
            out.append(f"<b>{to_html(match['s2'], urls)}</b>")
        elif match["em"]:
            out.append(f"<i>{to_html(match['e1'], urls)}</i>")
    out.append(html.escape(text[last:], quote=False))
    return "".join(out)


def to_markdown(translated, urls):
    """The translator's HTML back as Markdown"""
    text = re.sub(r'<span class="notranslate">(.*?)</span>', lambda m: m.group(1), translated, flags=re.S)
    text = re.sub(r'<a href="(\d+)">(.*?)</a>', lambda m: f"[{m.group(2)}]({urls[int(m.group(1))]})", text, flags=re.S)
    text = re.sub(r"<b>\s*<i>(.*?)</i>\s*</b>", r"***\1***", text, flags=re.S)
    text = re.sub(r"<b>(.*?)</b>", r"**\1**", text, flags=re.S)
    text = re.sub(r"<i>(.*?)</i>", r"*\1*", text, flags=re.S)
    return html.unescape(text)


def plan(page_text):
    """The page's lines: each kept as is, or (prefix, html, urls) to translate"""
    lines, in_code = [], False
    for line in page_text.split("\n"):
        if line.strip().startswith("```"):
            in_code = not in_code
            lines.append(line)
        elif in_code or not line.strip() or TABLE_SEPARATOR.match(line) or ONLY_TAGS.match(line):
            lines.append(line)
        else:
            prefix, body = PREFIX.match(line).groups()
            urls = []
            lines.append((prefix, to_html(body, urls), urls))
    return lines


def azure_translate(texts):
    """Each text in every language: {language: [translations, in order]}"""
    key, region = os.environ.get("AZURE_TRANSLATOR_KEY"), os.environ.get("AZURE_TRANSLATOR_REGION")
    if not key or not region:
        sys.exit("Set AZURE_TRANSLATOR_KEY and AZURE_TRANSLATOR_REGION (the Translator resource's key and location)")
    query = "&".join(["api-version=3.0", "from=en", "textType=html"] + [f"to={code}" for code in LANGUAGES])
    request = urllib.request.Request(
        f"{ENDPOINT}/translate?{query}",
        data=json.dumps([{"Text": text} for text in texts]).encode(),
        headers={"Ocp-Apim-Subscription-Key": key, "Ocp-Apim-Subscription-Region": region, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=60) as response:
            results = json.load(response)
    except urllib.error.HTTPError as error:
        raise RuntimeError(f"Azure Translator answered {error.code}: {error.read().decode(errors='replace')[:300]}") from error
    by_language = {code: [] for code in LANGUAGES}
    for result in results:
        for translation in result["translations"]:
            by_language[translation["to"]].append(translation["text"])
    return by_language


def translate_page(page_text, translator=azure_translate):
    """The page in every language: {language: Markdown}"""
    lines = plan(page_text)
    texts = [line[1] for line in lines if isinstance(line, tuple)]
    translated = translator(texts) if texts else {code: [] for code in LANGUAGES}
    pages = {}
    for code in LANGUAGES:
        pieces, results = [], iter(translated[code])
        for line in lines:
            if isinstance(line, tuple):
                prefix, _, urls = line
                pieces.append(prefix + to_markdown(next(results), urls))
            else:
                pieces.append(line)
        pages[code] = "\n".join(pieces)
    return pages


def english_pages():
    """The English pages: every .md file that isn't a translation (index.fr.md)"""
    return sorted(path for path in DOCS.rglob("*.md") if not any(path.name.endswith(f".{code}.md") for code in LANGUAGES))


def main():
    state = json.loads(STATE.read_text()) if STATE.exists() else {}
    done = 0
    for page in english_pages():
        key = str(page.relative_to(DOCS))
        text = page.read_text()
        digest = hashlib.sha256(text.encode()).hexdigest()
        targets = {code: page.with_name(f"{page.stem}.{code}.md") for code in LANGUAGES}
        if all(state.get(key, {}).get(code) == digest and targets[code].exists() for code in LANGUAGES):
            continue
        print(f"{key} -> fr, de, es", flush=True)
        try:
            pages = translate_page(text)
        except (RuntimeError, urllib.error.URLError) as error:
            print(f"  failed: {error}", file=sys.stderr)
            continue
        for code, translated in pages.items():
            targets[code].write_text(translated)
            state.setdefault(key, {})[code] = digest
        STATE.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")
        done += 1
    print(f"{done} pages translated" if done else "Every translation is up to date")


if __name__ == "__main__":
    main()
