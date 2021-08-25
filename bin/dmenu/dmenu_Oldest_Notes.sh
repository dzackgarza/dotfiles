#!/usr/bin/python

import os
import subprocess

CMD = 'find /home/zack/Notes/Obsidian -type f -iname "*.md" -exec stat -c "%X %n" {} \; | sort -n | sort -n | cut -d " " -f2-'

from os import popen
rows = popen(CMD).readlines()
basenames = [(r, os.path.basename(r)) for r in rows]

lookup = {}
for r in basenames:
  lookup[r[1]] =r[0]

#print(lookup)

justnames = list(map(lambda x: x[1], basenames))
everything = "".join(justnames)
result = subprocess.run(f"echo \"{everything}\" | dmenu -i", shell=True, stdout=subprocess.PIPE)
choice = result.stdout.decode('utf-8')
print(choice)

if choice not in lookup.keys():
  exit(0)

filename=lookup[choice]

new_filename=filename.rstrip().replace(r"'", r"\'")
subprocess.Popen(f"termite -e 'nvim \"{new_filename}\"'", shell=True)
