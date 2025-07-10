#!/usr/bin/env python3
"""
Unified Flashcard Generator for Anki (Markdown List Format)
- Reads a single markdown file with questions as top-level list items and answers as indented sub-list items
- Generates .apkg decks using genanki
- Optionally imports decks via AnkiConnect

Dependencies: genanki, requests
"""
import os
import sys
import argparse
import genanki
import requests

ANKI_API_URL = "http://localhost:8765"

import re

def parse_flashcard_markdown(filepath):
    notes = []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    question = None
    answer_lines = []
    q_pattern = re.compile(r'^-\s+(.*\S.*)$')
    a_pattern = re.compile(r'^[ \t]+-\s+(.*\S.*)$')
    for line in lines:
        q_match = q_pattern.match(line)
        a_match = a_pattern.match(line)
        if q_match:
            if question and answer_lines:
                notes.append((question, '\n'.join(answer_lines)))
            question = q_match.group(1).strip()
            answer_lines = []
        elif a_match:
            answer_lines.append(a_match.group(1).strip())
        elif line.strip() == '':
            continue
        else:
            # Ignore lines that are not part of a list
            continue
    if question and answer_lines:
        notes.append((question, '\n'.join(answer_lines)))
    return notes

def create_anki_deck(deck_name, notes):
    model = genanki.Model(
        1607392319,
        'Simple Model',
        fields=[{'name': 'Question'}, {'name': 'Answer'}],
        templates=[{
            'name': 'Card 1',
            'qfmt': '{{Question}}',
            'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
        }],
        css=".card { font-family: 'Arial'; font-size: 20px; }"
    )
    deck = genanki.Deck(hash(deck_name) & 0xFFFFFFFF, deck_name)
    for q, a in notes:
        deck.add_note(genanki.Note(model=model, fields=[q, a]))
    return deck


def main():
    parser = argparse.ArgumentParser(description="Unified Anki Flashcard Generator (Markdown List Format)")
    parser.add_argument("input_file", help="Input markdown file with flashcards (questions as list items, answers as sub-list items)")
    parser.add_argument("--output", help="Output .apkg file (default: deck name)")
    parser.add_argument("--import", dest="do_import", action="store_true", help="Import deck via AnkiConnect API")
    args = parser.parse_args()

    notes = parse_flashcard_markdown(args.input_file)
    if not notes:
        print("No flashcards found.")
        sys.exit(1)
    deck_name = os.path.splitext(os.path.basename(args.input_file))[0]
    deck = create_anki_deck(deck_name, notes)
    apkg_path = args.output or f"{deck_name}.apkg"
    genanki.Package(deck).write_to_file(apkg_path)
    print(f"Deck written to {apkg_path}")

    if args.do_import:
        response = requests.post(ANKI_API_URL, json={
            "action": "importPackage",
            "version": 6,
            "params": {"path": os.path.abspath(apkg_path)}
        })
        print("AnkiConnect import response:", response.text)

if __name__ == "__main__":
    main()
