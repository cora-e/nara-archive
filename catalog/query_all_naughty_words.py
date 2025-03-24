#!/usr/bin/env python

import os
import sys
from multiprocessing import Pool
from functools import partial

import json
import tqdm

# Superset words because fascists are unimaginative:
# biased toward
# biases towards
# females
# implicit biases

naughty = [
    "activism",
    "activists",
    "advocacy",
    "advocate",
    "advocates",
    "barrier",
    "barriers",
    "biased",
    "biases",
    "bipoc",
    "latinx",
    #"black and latinx", # TODO 
    "community diversity",
    "community equity",
    "cultural differences",
    "cultural heritage",
    "culturally responsive",
    "disabilities",
    "disability",
    "discriminated",
    "discrimination",
    "discriminatory",
    "diverse backgrounds",
    "diverse communities",
    "diverse community",
    "diverse group",
    "diverse groups",
    "diversified",
    "diversify",
    "diversifying",
    "diversity and inclusion",
    "diversity equity",
    "enhance the diversity",
    "enhancing diversity",
    "equal opportunity",
    "equality",
    "equitable",
    "equity",
    "ethnicity",
    "excluded",
    "female",
    "fostering inclusivity",
    "gender",
    "gender diversity",
    "genders",
    "hate speech",
    "hispanic minority",
    "historically",
    "implicit bias",
    "inclusion",
    "inclusive",
    "inclusiveness",
    "inclusivity",
    "increase diversity",
    "increase the diversity",
    "indigenous community",
    "inequalities",
    "inequality",
    "inequitable",
    "inequities",
    "institutional",
    "lgbt",
    "marginalize",
    "marginalized",
    "minorities",
    "minority",
    "multicultural",
    "polarization",
    "political",
    "prejudice",
    "privileges",
    "promoting diversity",
    "race and ethnicity",
    "racial",
    "racial diversity",
    "racial inequality",
    "racial justice",
    "racially",
    "racism",
    "sense of belonging",
    "sexual preferences",
    "social justice",
    "sociocultural",
    "socioeconomic",
    "status",
    "stereotypes",
    "systemic",
    "trauma",
    "under appreciated",
    "under represented",
    "under served",
    "underrepresentation",
    "underrepresented",
    "underserved",
    "undervalued",
    "victim",
    "women",
    "women and underrepresented"
    ]

def is_naughty(fname):
    for word in naughty:
        grep(fname, word)

def is_naughty(fname):
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
                for word in naughty:
                    if ('scopeAndContentNote' in rec and word in rec['scopeAndContentNote'].lower()) or \
                        ('title' in rec and word in rec['title'].lower()) or \
                        ('extractedText' in rec and word in rec['extractedText'].lower()) or \
                        ('objectDescription' in rec and word in rec['objectDescription'].lower()):
                        hit = True

                    if 'digitalObjects' in rec:
                        for dobj in rec['digitalObjects']:
                            if ('scopeAndContentNote' in dobj and word in dobj['scopeAndContentNote'].lower()) or \
                                ('title' in dobj and word in rec['title'].lower()) or \
                                ('extractedText' in dobj and word in dobj['extractedText'].lower()) or \
                                ('objectDescription' in dobj and word in dobj['objectDescription'].lower()):
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
        hits_per_file = list(tqdm.tqdm(p.imap(is_naughty, all_files), total=len(all_files)))
    

    all_hits = []
    for hits in hits_per_file:
        all_hits.extend(hits)

    with open(f"urls_all_naughty_words.txt", "w") as outf:
        for hit in all_hits:
            outf.write(hit+"\n")

    print(f"Total URLs: {len(all_hits)}")