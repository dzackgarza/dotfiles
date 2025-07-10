import zipfile
import sqlite3
import os
import sys

APKG_PATH = os.path.join(os.path.dirname(__file__), 'output', 'test_deck.apkg')
EXPECTED_QUESTIONS = [
    'What is the quadratic formula?',
    'Who was the first president of the United States?',
    'What is the capital of France?'
]
EXPECTED_ANSWERS = [
    '$x = \\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}$\nUsed to solve $ax^2 + bx + c = 0$',
    'George Washington',
    'Paris\n(It\'s not Lyon or Marseille.)'
]
EXPECTED_IMAGE = 'quadratic.png'  # If you add an image card

# 1. Check that the .apkg is a valid zip and contains expected files
assert os.path.exists(APKG_PATH), f"APKG not found: {APKG_PATH}"
with zipfile.ZipFile(APKG_PATH, 'r') as zf:
    namelist = zf.namelist()
    assert 'collection.anki2' in namelist, "collection.anki2 missing from apkg"
    assert 'media' in namelist, "media file missing from apkg"
    # Optionally check for image file in media
    # media_map = zf.read('media').decode('utf-8')
    # assert any(EXPECTED_IMAGE in v for v in media_map.values()), "Expected image not found in media map"

    # 2. Extract collection.anki2 to a temp location
    zf.extract('collection.anki2', '/tmp')

# 3. Open the SQLite DB and check for expected questions/answers
conn = sqlite3.connect('/tmp/collection.anki2')
c = conn.cursor()
c.execute('SELECT flds FROM notes')
notes = c.fetchall()
conn.close()

# Each note's fields are separated by 0x1f (unit separator)
found_questions = []
found_answers = []
for (flds,) in notes:
    parts = flds.split('\x1f')
    if len(parts) >= 2:
        found_questions.append(parts[0].strip())
        found_answers.append(parts[1].strip())

for q in EXPECTED_QUESTIONS:
    assert q in found_questions, f"Missing question: {q}"
for a in EXPECTED_ANSWERS:
    assert any(a in ans for ans in found_answers), f"Missing answer: {a}"

print("Test passed: All expected questions and answers found in deck.")
# Optionally, check for LaTeX
assert any('$x =' in ans for ans in found_answers), "LaTeX math not found in answers."
print("Test passed: LaTeX math found in answers.")
# Optionally, check for image inclusion in media (if you add an image card)
# print("Test passed: Image found in media.")
