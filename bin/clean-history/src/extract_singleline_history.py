import re

input_file = '/home/dzack/dotfiles/bin/zsh_history_testcopy'
output_file = '/home/dzack/dotfiles/bin/zsh_history_testcopy_extracted'

# List of trivial/noisy commands to ignore (configurable)
NOISE = {'ls', 'pwd', 'exit', 'clear', 'history'}

with open(input_file, encoding='latin1') as f, open(output_file, 'w', encoding='utf-8') as out:
    for line in f:
        m = re.match(r'^: \d+:\d+;(.*)$', line.rstrip())
        if m:
            cmd = m.group(1).strip()
            # Skip if command is empty or contains newlines (multiline)
            if not cmd or '\n' in cmd or '\\' in cmd:
                continue
            # Skip trivial/noisy commands (exact or prefix match)
            if any(cmd == n or cmd.startswith(n + ' ') for n in NOISE):
                continue
            out.write(line)
