#!/usr/bin/env python3

from PIL import Image
import os, sys
from inspect import getsourcefile

cwd = os.getcwd() + "/Course6/Project4 - Update Catalog/supplier-data/images/"

def convert(infile):
    f, e = os.path.splitext(infile)
    outfile = f + '.jpg'
    with Image.open(cwd + infile).convert("RGB").resize(size=[600, 400]) as im:
        im.save(cwd + outfile, 'jpeg')

def main(argv):
    for item in os.listdir(cwd):
        convert(item)

if __name__ == "__main__":
    main(sys.argv)