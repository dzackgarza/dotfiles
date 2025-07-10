# Flashcards Unified

A modern, maintainable workflow for generating Anki decks from Markdown files with YAML frontmatter.

## Directory Structure

- `src/` — Main Python code (`flashcards_unified.py`)
- `docs/` — Documentation
- `tests/` — Test scripts and outputs
  - `test_data/` — Sample flashcard markdown files for testing

## Quickstart

1. **Install dependencies using PDM:**

```sh
pdm install
```

2. **Run the unified script:**

```sh
pdm run python src/flashcards_unified.py tests/test_data --output tests/output/test_deck.apkg --copy-images
```

3. **Run the test script:**

```sh
pdm run bash tests/test_flashcards_unified.sh
```


## Flashcard List Format

All flashcards are stored in a single plain text file. Each flashcard consists of a question line (not indented), followed by one or more indented answer lines. No YAML, no frontmatter, no one-file-per-card.



**Example:**

```markdown
- What is the quadratic formula?
    - $x = \frac{-b \pm \sqrt{b^2-4ac}}{2a}$
    - Used to solve $ax^2 + bx + c = 0$
- Who was the first president of the United States?
    - George Washington
- What is the capital of France?
    - Paris
    - (It's not Lyon or Marseille.)
```


- Each top-level list item (`- ...`) is a question.
- Each indented sub-list item (`    - ...`) is an answer line for the previous question.
- Answers can be multiline (just keep indenting as sub-list items).
- Math should be written as valid LaTeX within `$...$` or `$$...$$` for compatibility with Anki/Markdown.

This format is simple, fast to edit, and works well for both text and code flashcards.

## Features
- Scans directories for all `.md` files with `flashcard:` in frontmatter
- Extracts images and copies them to Anki media
- Generates `.apkg` decks using `genanki`
- Optionally imports decks via AnkiConnect

## License
MIT
