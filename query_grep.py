#!/usr/bin/env python

import os
import sys
from multiprocessing import Pool
from functools import partial

import json
import tqdm

# TODO track number of matches separate from number of URLs (multiple per match sometimes)

def grep(fname, query_string):
    #print(fname)
    if not '.jsonl' in fname:
        return 0
    hits = []
    with open(fname, 'r') as file:
        for line in file:
            parsed = json.loads(line)
            if 'record' in parsed:
                rec = parsed['record']
                hit = False
                if ('scopeAndContentNote' in rec and query_string in rec['scopeAndContentNote']) or \
                    ('title' in rec and query_string in rec['title']) or \
                    ('extractedText' in rec and query_string in rec['extractedText']) or \
                    ('objectDescription' in rec and query_string in rec['objectDescription']):
                    hit = True

                if 'digitalObjects' in rec:
                    for dobj in rec['digitalObjects']:
                        if ('scopeAndContentNote' in dobj and query_string in dobj['scopeAndContentNote']) or \
                            ('title' in dobj and query_string in rec['title']) or \
                            ('extractedText' in dobj and query_string in dobj['extractedText']) or \
                            ('objectDescription' in dobj and query_string in dobj['objectDescription']):
                            hit = True

                if hit:
                    if 'digitalObjects' in rec:
                        for dobj in rec['digitalObjects']:
                            if 'objectUrl' in dobj:
                                hits.append(dobj['objectUrl'])
                    else:
                        if 'localIdentifier' in rec:
                            print(f"Match w/o URLs: localID:{rec['localIdentifier']} naID:{rec['naId']}")
                        else:
                            print(f"Match w/o URLs: naID:{rec['naId']}")

    return hits

if __name__ == '__main__':
    # Walk filesystem for all filenames
    all_files = []
    for root, dirs, files in os.walk(sys.argv[1]):
        all_files.extend([os.path.join(root, f) for f in files])

    # Multiprocess file contents for speed
    with Pool(56) as p:
        hits_per_file = list(tqdm.tqdm(p.imap(partial(grep, query_string=sys.argv[2]), all_files), total=len(all_files)))
    

    all_hits = []
    for hits in hits_per_file:
        all_hits.extend(hits)

    with open(f"urls_{sys.argv[2]}.txt", "w") as outf:
        for hit in all_hits:
            outf.write(hit+"\n")

    print(f"Total URLs: {len(all_hits)}")