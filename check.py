#!/usr/bin/env python3

# usage - python3 check.py <command> `ls src/*.adoc`

import sys
import re

script_cmd = sys.argv[1]

pattern = re.compile(r'\[\[(SWRS-[xX]{3}-.*?)\]\]')
if script_cmd == "--check":
    pattern = re.compile(r'\[\[(SWRS-[0-9]{3}-.*?)\]\]')

tags = {}
tags_duplicate = {}

for filepath in sys.argv[2:]:
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
        for tag in pattern.findall(text):
            tags.setdefault(tag, re.sub(r'[xX]{3}', str(len(tags)).zfill(3), tag))
            tags_duplicate.setdefault(tag, []).append(filepath)

duplicate_error = False

for tag in tags_duplicate:
    if len(tags_duplicate[tag]) > 1:
        duplicate_error = True
        print("!!! ERROR DUPLICATE: ", tag, " : ", tags_duplicate[tag])
    
if duplicate_error:
    sys.exit(1)

from pprint import pprint
print(*tags.keys(), sep='\n')
#pprint(tags)
#pprint(tags_duplicate)

if script_cmd != "--replace":
    sys.exit(0)

for filepath in sys.argv[2:]:
    print(">> Processing: ", filepath)
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()
        new_text = text
        for tag in tags:
            new_text = new_text.replace(tag, tags[tag])
        if new_text != text:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(new_text)
        else:
            print(">>> no change")
