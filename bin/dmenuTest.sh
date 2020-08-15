#!/usr/bin/python

import os
import subprocess

CMD = 'find /home/zack/Dropbox/Library -type f -iname "*.pdf" -exec stat -c "%X %n" {} \; | sort -n | tail -30 | sort -nr | cut -d " " -f2-'

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

subprocess.Popen(f"okular \"{filename}\"", shell=True)
