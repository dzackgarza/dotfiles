"""Protect and restore Obsidian wikilinks ([[...]])."""

import re

WIKILINK_PATTERN = re.compile(r"\[\[.*?\]\]")


def protect_wikilinks(text: str) -> str:
    """Replace wikilinks with opaque placeholders, storing originals.

    Returns text with wikilinks replaced by __ZMD_WIKILINK_N__ tokens.
    Metadata is stored on the function for restore_wikilinks.
    """
    _wikilink_store.clear()
    replacements: dict[str, str] = {}

    def replace(match):
        idx = len(_wikilink_store)
        token = f"__ZMD_WIKILINK_{idx}__"
        _wikilink_store.append(match.group(0))
        replacements[match.group(0)] = token
        return token

    text = WIKILINK_PATTERN.sub(replace, text)
    return text


def restore_wikilinks(text: str) -> str:
    """Restore wikilinks from placeholders."""
    for idx, original in enumerate(_wikilink_store):
        token = f"__ZMD_WIKILINK_{idx}__"
        text = text.replace(token, original)
    _wikilink_store.clear()
    return text


_wikilink_store: list = []
