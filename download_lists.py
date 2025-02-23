#!/usr/bin/env python

import os
import sys

import tqdm
from urllib.request import urlretrieve
from multiprocessing import Pool

def ensure(url):
    url_split = url.split('/')
    filename = "/".join(url_split[url_split.index("NARAprodstorage")+1:])
    foldername = "/".join(url_split[url_split.index("NARAprodstorage")+1:-1])
    if not os.path.exists(filename):
        os.makedirs(foldername, exist_ok=True)
        urlretrieve(url, filename)

if __name__ == "__main__":
    urls = []
    for fname in sys.argv[1:]:
        with open(fname, 'r') as fil:
            for line in fil:
                urls.append(line[:-1])

    print(f"Downloading {len(urls)} files.")

    # Multiprocess file contents for speed
    with Pool(20) as p:
       list(tqdm.tqdm(p.imap(ensure, urls), total=len(urls)))