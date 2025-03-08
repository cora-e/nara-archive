#!/usr/bin/env python

import os
import sys

import tqdm
from multiprocessing import Pool

import boto3
import botocore
from botocore import UNSIGNED
from botocore.client import Config

#s3_client = boto3.client("s3", config=Config(signature_version=UNSIGNED))

def ensure(url):
    url_split = url.split('/')
    filename = "/".join(url_split[url_split.index("NARAprodstorage")+1:])
    foldername = "/".join(url_split[url_split.index("NARAprodstorage")+1:-1])
    # We got boston separately
    if not os.path.exists(filename) and not "/boston/" in filename:
        s3_client = boto3.client("s3", config=Config(signature_version=UNSIGNED))
        os.makedirs(foldername, exist_ok=True)
        attempt = 0
        while attempt < 5:
            try:
                print(f"Downloading {filename}")
                response = s3_client.get_object(
                    Bucket = "NARAprodstorage",
                    Key = filename
                )
                with open(filename, "wb") as fil:
                    fil.write(response["Body"].read())
                break
            except botocore.exceptions.ReadTimeoutError as e:
                attempt += 1
                print(e)
                print(f"Continuing (attempt {attempt})...")
            except botocore.exceptions.ClientError as e:
                attempt += 1
                print(e)
                print(f"Continuing (attempt {attempt})...")
            except botocore.exceptions.ResponseStreamingError as e:
                attempt += 1
                print(e)
                print(f"Continuing (attempt {attempt})...")

if __name__ == "__main__":
    urls = []
    for fname in sys.argv[1:]:
        with open(fname, 'r') as fil:
            for line in fil:
                urls.append(line[:-1])

    print(f"Downloading {len(urls)} files.")

    # Multiprocess file contents for speed
    # tqdm is weird about timings or would be list(tqdm.tqdm(), total=len(urls))
    with Pool(20) as p:
       list(p.imap(ensure, urls))
