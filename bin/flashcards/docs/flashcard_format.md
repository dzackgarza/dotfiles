# Flashcard Markdown Format

Each flashcard is a Markdown file with YAML frontmatter. The frontmatter must include a `flashcard:` field, which is used as the question. The body of the file is used as the answer.

## Example

```markdown
---
flashcard: What is the quadratic formula?
---
The quadratic formula is:

$$x = \frac{-b \pm \sqrt{b^2-4ac}}{2a}$$

![](images/quadratic.png)
```

- You can include LaTeX, images, and attachments in the answer.
- Images referenced in the markdown will be copied to the Anki media collection if `--copy-images` is used.

## Requirements
- The file must have a `flashcard:` field in the YAML frontmatter.
- The answer can contain Markdown, LaTeX, and image links.
- Each file = one card.
