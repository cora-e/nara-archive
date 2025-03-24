#!/usr/bin/env python3

import os
import PyPDF2

# traverse root directory, and list directories as dirs and files as files
for root, dirs, files in os.walk("."):
    path = root.split(os.sep)
    print((len(path) - 1) * '---', os.path.basename(root))

    imgs = [f for f in files if ".jpg" in f or ".tif" in f or ".png" in f]
    pdfs = [f for f in files if ".pdf" in f]

    if len(pdfs) == 1 and len(imgs) > 0:
        pdf_file = open(root+os.sep+pdfs[0], 'rb')
        npages = len(PyPDF2.PdfReader(pdf_file).pages)
        page_imgs = [i for i in imgs if pdfs[0].replace(".pdf","") in i]
        print(f"Pages: {npages} Page images: {len(page_imgs)}")
        if len(page_imgs) <= npages: # check the PDF contains more than we're deleting
            print(f"Deleting {len(page_imgs)} files")
            for img in page_imgs:
                os.remove(root+os.sep+img)

