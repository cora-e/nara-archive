#!/usr/bin/env python

import os
import sys
from multiprocessing import Pool

import json
import tqdm

def count(fname):
    #print(fname)
    if not '.jsonl' in fname:
        return 0
    nurls = 0
    with open(fname, 'r') as file:
        for line in file:
            parsed = json.loads(line)
            if 'record' in parsed and 'digitalObjects' in parsed['record']:
                for dobj in parsed['record']['digitalObjects']:
                    #print(dobj['objectUrl'])
                    nurls += 1
    return nurls

if __name__ == '__main__':
    # Walk filesystem for all filenames
    all_files = []
    for root, dirs, files in os.walk(sys.argv[1]):
        all_files.extend([os.path.join(root, f) for f in files])

    # Multiprocess file contents for speed
    with Pool(56) as p:
        counts = list(tqdm.tqdm(p.imap(count, all_files), total=len(all_files)))
    
    nurls_tot = 0
    for c in counts:
        nurls_tot += c
    print(nurls_tot)