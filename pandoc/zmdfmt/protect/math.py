"""Protect and restore math regions (display and inline)."""

import re

# Match display math \[...\] blocks (multiline, non-greedy on body)
DISPLAY_MATH = re.compile(r"\\\[(.*?)\\\]", re.DOTALL)

# Match inline math $...$ (single-line, avoids $$)
INLINE_MATH = re.compile(r"(?<!\$)\$(?!\$)(.*?)(?<!\$)\$(?!\$)")


_math_store: list[str] = []


def protect_math(text: str) -> str:
    """Replace math regions with placeholders, storing originals."""
    _math_store.clear()

    def replace_display(match):
        idx = len(_math_store)
        token = f"__ZMD_MATH_{idx}__"
        _math_store.append(match.group(0))
        return token

    def replace_inline(match):
        idx = len(_math_store)
        token = f"__ZMD_MATH_{idx}__"
        _math_store.append(match.group(0))
        return token

    text = DISPLAY_MATH.sub(replace_display, text)
    text = INLINE_MATH.sub(replace_inline, text)
    return text


def restore_math(text: str) -> str:
    """Restore math regions from placeholders."""
    for idx, original in enumerate(_math_store):
        token = f"__ZMD_MATH_{idx}__"
        text = text.replace(token, original)
    _math_store.clear()
    return text
