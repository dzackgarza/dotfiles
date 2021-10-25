#!/usr/bin/env python

import re
import sys

regex = r"\\\[\\\[(.*?)\\\]\\\]"
subst = "[\\1](\\1.md)"

# You can manually specify the number of replacements by changing the 4th argument
test_str = sys.stdin.readline()
result = re.sub(regex, subst, test_str, 0)

if result:
    print(result)
else:
    print("Error")
