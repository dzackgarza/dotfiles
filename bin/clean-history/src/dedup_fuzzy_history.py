import re
from rapidfuzz import fuzz

input_file = '/home/dzack/dotfiles/bin/zsh_history_testcopy_extracted'
output_file = '/home/dzack/dotfiles/bin/zsh_history_testcopy_deduped'
SIMILARITY_THRESHOLD = 90

entries = []
commands = []
with open(input_file, encoding='utf-8') as f:
    for line in f:
        m = re.match(r'^: \d+:\d+;(.*)$', line.rstrip())
        if m:
            cmd = m.group(1).strip()
            entries.append(line)
            commands.append(cmd)

kept = []
kept_entries = []
for i, cmd in enumerate(commands):
    is_similar = False
    for prev in kept:
        if fuzz.ratio(cmd, prev) >= SIMILARITY_THRESHOLD:
            is_similar = True
            break
    if not is_similar:
        kept.append(cmd)
        kept_entries.append(entries[i])

with open(output_file, 'w', encoding='utf-8') as f:
    for entry in kept_entries:
        f.write(entry)
