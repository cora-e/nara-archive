#!/usr/bin/env python3

import os
import sys
import PyPDF2

tot_npages = 0
for file in sys.argv[1:]:
    pdf_file = open(file, 'rb')
    npages = len(PyPDF2.PdfFileReader(pdf_file).pages)
    print(f"Pages: {npages}")
    tot_npages += npages

print(f"Total pages: {tot_npages}")
