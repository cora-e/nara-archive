#!/usr/bin/env python3

import os
import PyPDF2

import boto3
import botocore
from botocore import UNSIGNED
from botocore.client import Config

def list_dir(path):
    client = boto3.client("s3", config=Config(signature_version=UNSIGNED))
    pages = client.get_paginator("list_objects_v2").paginate(Bucket='NARAprodstorage', Prefix=path)
    keys = []
    for p in pages:
        if 'Contents'in p:
            for e in p['Contents']:
                keys.append(e['Key'])
    return keys

def ensure(filename):
    # Downloads to current directory
    path = filename.split('/')
    foldername = "/".join(path[:-1])
    write_fname = path[-1]
    # Always download, we're only called to either download or *replace*
    client = boto3.client("s3", config=Config(signature_version=UNSIGNED))
    os.makedirs(foldername, exist_ok=True)
    attempt = 0
    while attempt < 5:
        try:
            print(f"Downloading {filename}")
            response = client.get_object(
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

# traverse root directory
for root, dirs, files in os.walk("."):
    path = root.split(os.sep)
    print((len(path) - 1) * '---', os.path.basename(root))

    # Check if there are images, list
    imgs = [f for f in files if ".jpg" in f or ".jpeg" in f or ".tif" in f or ".png" in f]

    # If there are...
    if len(imgs) > 0:
        pdfs = [f for f in files if ".pdf" in f]

        # If no PDF in dir, check if we can fetch one
        if len(pdfs) < 1:
            folder = root[2:]
            pdfs_online = [f for f in list_dir(folder) if ".pdf" in f]
            # Most folders are 1 PDF, lots of images (known exceptions exist!). Warn if not
            if len(pdfs_online) > 1:
                print("WARNING downloading multiple PDF files!")
            # Sometimes an image sneaks into a root folder and we really
            # don't want *everything* in that folder. Limit to the n of images
            if len(pdfs_online) < len(imgs):
                for pdf in pdfs_online:
                    ensure(pdf)
                # local filenames in curdir
                pdfs = [f.split("/")[-1] for f in pdfs_online]

        # TODO this will need to accommodate multi-PDF+contents folders, but these seem rare?
        # Also it's not universal that the PDF name is a part of the image names --
        # sometimes it's the last-named file in the upload
        if len(pdfs) == 1 and os.path.isfile(root+os.sep+pdfs[0]):
            # Anything named a superset of the pdf name
            page_imgs = [i for i in imgs if pdfs[0].replace(".pdf","") in i]
            # If there are any potentially delete-able images
            if len(page_imgs) > 0:
                # PDF itself
                # Some downloads are corrupt apparently?  So uh, redo those
                attempts = 0
                while attempts < 3:
                    try:
                        pdf_file = open(root+os.sep+pdfs[0], 'rb')
                        npages = len(PyPDF2.PdfReader(pdf_file).pages)
                        break
                    except:
                        ensure(root[2:]+os.sep+pdfs[0])
                        attempts += 1
                # If it's really borked, at least don't delete the images!
                if attempts == 3:
                    npages = 0

                # Check we're not deleting more than the PDF's page count, that would be bad
                print(f"PDF Pages: {npages} Image Pages: {len(page_imgs)}")
                if len(page_imgs) <= npages:
                    print(f"Deleting {len(page_imgs)} files")
                    for img in page_imgs:
                        os.remove(root+os.sep+img)

