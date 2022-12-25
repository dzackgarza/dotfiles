#!/usr/bin/python

import genanki
import argparse
import misaka
import subprocess
import re
import sys
import os
import frontmatter
from urllib.parse import unquote
import textwrap

# Parse the command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("input", help="The input markdown file")
parser.add_argument("output", help="The output Anki deck file")
args = parser.parse_args()

def extract_flashcard_field(filename: str) -> str:
    # Read the file and extract the front matter
    with open(filename, 'r') as f:
        post = frontmatter.load(f)

    # Extract the "flashcard" field from the front matter
    flashcard = post['flashcard']

    return flashcard

filename = args.input
filename = os.path.basename(filename)
# Replace the extension on the filename
root, _ = os.path.splitext(filename)
flashcard_title = extract_flashcard_field(filename)


CARD_MATHJAX_CONTENT = textwrap.dedent(r"""
<script>
MathJax.config.tex.macros = {
	coloneqq: ['\\mathrel{\\vcenter{:}}=', 0],
    qty: ['{\\left( {#1} \\right)}', 1],
    divides: ["{~\\Bigm| ~}", 0]
};
MathJax.startup.getComponents();
</script>
""")

# Create a new Genanki NoteModel to represent each flashcard
model = genanki.Model(
  1607392319,
  root,
  fields=[
    {'name': 'Question'},
    {'name': 'Answer'},
  ],
  templates=[
    {
      'name': 'Card 1',
      'qfmt': "{{{{Question}}}}\n{0}".format(CARD_MATHJAX_CONTENT),
      'afmt': "{{{{Question}}}}<hr id='answer'>{{{{Answer}}}}\n{0}".format(CARD_MATHJAX_CONTENT),
    },
  ],
)

# Create a new Genanki Deck to hold the flashcards
deck = genanki.Deck(
  2059400110,
  flashcard_title
)

def delete_checkboxes(s):
  pattern = r'-\s*\[\s?[x]?\]\s?'
  r1 = re.sub(pattern, '', s)
  return r1

def delete_stuff(s):
  # Use a regular expression to match substrings of the form "[ ]" or "[x]"
  # Remove hashtags
  pattern = r'\B#\w+'
  r2 = re.sub(pattern, '', s)
  # Remove dates
  pattern = r'\d{4}-\d{2}-\d{2}'
  r3 = re.sub(pattern, '', r2).strip()
  # Remove unicode
  pattern = r'[^\x00-\x7F]+'
  return re.sub(pattern, '', r3).replace("[[", '').replace("]]", '')

def field_to_html(field):
    for bracket in ["(", ")", "[", "]"]:
        field = field.replace(r"\{}".format(bracket), r"\\{}".format(bracket))
    return unquote(misaka.html(delete_checkboxes(field), extensions=("fenced-code", "math")))

def run_external_program(filename):
  # Open the file and read its contents
  with open(filename, 'r') as f:
    input_data = f.read()

  # Use the subprocess module to run an external program and
  # pass the file contents as input
  temp_align = bytes(delete_stuff(input_data), encoding="raw_unicode_escape")
  result = subprocess.run(['pandoc_stripmacros.sh'], input=temp_align, stdout=subprocess.PIPE)

  # Return the output as a generator that yields lines one at a time
  return result.stdout.decode('utf-8').split('\n')

lines = run_external_program(filename)

# Parse the file and create flashcards
question = None
answer = ''
for line in lines:
  # print(line)
  # If the line is unindented, it is a new question
  if not line.startswith(' ') and not line.startswith('\t'):
    # If the previous line was an indented answer, create a flashcard
    if question and answer:
      flashcard = genanki.Note(model=model, fields=[field_to_html(question), field_to_html(answer) ])
      deck.add_note(flashcard)
    question = line.strip()
    answer = ''
  # If the line is indented, it is part of the answer
  else:
    # print("Found indented line, adding answer")
    answer += line.strip() + '\n'

# If the last line of the file is an indented answer, create a flashcard
if question and answer:
  flashcard = genanki.Note(model=model, fields=[field_to_html(question), field_to_html(answer) ])
  deck.add_note(flashcard)


# Write the deck to a file
genanki.Package(deck).write_to_file(args.output)
