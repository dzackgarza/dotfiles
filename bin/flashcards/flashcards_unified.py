#!/usr/bin/env python3
"""
Unified Flashcard Generator for Anki
- Scans a directory for markdown files with 'flashcard:' in frontmatter
- Extracts flashcard content and images
- Copies images to Anki media collection
- Generates .apkg decks using genanki
- Optionally interacts with AnkiConnect API

Dependencies: genanki, python-frontmatter, mistune, requests
"""
import os
import sys
import argparse
import frontmatter
import mistune
import shutil
import subprocess
import glob
import genanki
import requests
from urllib.parse import unquote

ANKI_MEDIA_DIR = os.path.expanduser("~/.local/share/Anki2/User 1/collection.media")
ANKI_ATTACHMENTS_DIR = os.path.join(ANKI_MEDIA_DIR, "attachments")
ANKI_API_URL = "http://localhost:8765"


def find_markdown_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):
                yield os.path.join(root, file)

def extract_flashcard_field(filename):
    post = frontmatter.load(filename)
    return post.get('flashcard', None), post.content

def extract_image_links(markdown_text):
    """
    Extract image URLs from markdown using Mistune 3.x AST.
    """
    image_links = []
    md = mistune.create_markdown(renderer="ast")
    ast = md(markdown_text)
    def walk(node):
        if isinstance(node, dict):
            if node.get('type') == 'image' and 'attrs' in node and 'url' in node['attrs']:
                image_links.append(node['attrs']['url'])
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for item in node:
                walk(item)
    walk(ast)
    return image_links

def locate_and_copy_image(image_url, copy=True):
    image_file = os.path.basename(unquote(image_url))
    # Use locate or glob to find the file
    try:
        result = subprocess.check_output(["locate", image_file], text=True)
        candidates = [line for line in result.splitlines() if "collection" not in line and "Trash" not in line]
    except Exception:
        candidates = []
    if not candidates:
        # Fallback: try glob in home directory
        candidates = glob.glob(os.path.expanduser(f"~/**/{image_file}"), recursive=True)
    if candidates:
        target_dir = ANKI_ATTACHMENTS_DIR if "attachment" in image_url else ANKI_MEDIA_DIR
        os.makedirs(target_dir, exist_ok=True)
        if copy:
            shutil.copy2(candidates[0], target_dir)
        return os.path.join(target_dir, image_file)
    return None

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
    parser = argparse.ArgumentParser(description="Unified Anki Flashcard Generator")
    parser.add_argument("input_dir", help="Directory to scan for markdown files")
    parser.add_argument("--output", help="Output .apkg file (default: deck name)")
    parser.add_argument("--copy-images", action="store_true", help="Copy images to Anki media collection")
    parser.add_argument("--import", dest="do_import", action="store_true", help="Import deck via AnkiConnect API")
    args = parser.parse_args()

    notes = []
    deck_name = os.path.basename(os.path.abspath(args.input_dir))
    for md_file in find_markdown_files(args.input_dir):
        flashcard, content = extract_flashcard_field(md_file)
        if not flashcard:
            continue
        # For simplicity, treat the whole content as the answer
        question = flashcard
        answer = content
        # Extract and optionally copy images
        image_links = extract_image_links(content)
        for img in image_links:
            locate_and_copy_image(img, copy=args.copy_images)
        notes.append((question, answer))

    if not notes:
        print("No flashcards found.")
        sys.exit(1)
    deck = create_anki_deck(deck_name, notes)
    apkg_path = args.output or f"{deck_name}.apkg"
    genanki.Package(deck).write_to_file(apkg_path)
    print(f"Deck written to {apkg_path}")

    if args.do_import:
        # Import via AnkiConnect
        with open(apkg_path, "rb") as f:
            data = f.read()
        response = requests.post(ANKI_API_URL, json={
            "action": "importPackage",
            "version": 6,
            "params": {"path": apkg_path}
        })
        print("AnkiConnect import response:", response.text)

if __name__ == "__main__":
    main()
