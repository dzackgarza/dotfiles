"""Ensure exactly one final newline."""


def ensure_final_newline(text: str) -> str:
    """Ensure text ends with exactly one newline."""
    text = text.rstrip("\n")
    return text + "\n"
