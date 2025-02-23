#!/usr/bin/env python

import os
import sys
from multiprocessing import Pool
from functools import partial

import json
import tqdm

# TODO track number of matches separate from number of URLs (multiple per match sometimes)

def grep(fname, naid):
    #print(fname)
    if not '.jsonl' in fname:
        return 0
    hits = []
    with open(fname, 'r') as file:
        for line in file:
            parsed = json.loads(line)
            if 'record' in parsed:
                if int(parsed['record']['naId']) == int(naid):
                    print(parsed['record'])

    return hits

if __name__ == '__main__':
    # Walk filesystem for all filenames
    all_files = []
    for root, dirs, files in os.walk(sys.argv[1]):
        all_files.extend([os.path.join(root, f) for f in files])

    # Multiprocess file contents for speed
    with Pool(56) as p:
        list(tqdm.tqdm(p.imap(partial(grep, naid=sys.argv[2]), all_files), total=len(all_files)))
