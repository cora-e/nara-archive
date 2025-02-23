#!/usr/bin/env python

import os
import json

all_files = []

# Walk filesystem for all filenames
for root, dirs, files in os.walk("."):
    all_files.extend([os.path.join(root, f) for f in files])

# Iterate through files, counting urls when present
nurls = 0
for fname in all_files:
    print(fname)
    if '.py' in fname:
        continue
    with open(fname, 'r') as file:
        for line in file:
            parsed = json.loads(line)
            if 'record' in parsed and 'digitalObjects' in parsed['record']:
                for dobj in parsed['record']['digitalObjects']:
                    #print(dobj['objectUrl'])
                    nurls += 1

print(nurls)