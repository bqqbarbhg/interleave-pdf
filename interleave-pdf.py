#!/usr/bin/env python3

import img2pdf
import argparse
import glob
import re

parser = argparse.ArgumentParser(description="Interleave a series of images to a pdf.")
parser.add_argument("-s", metavar=".jpg", action="append", nargs="+", help="Input page range")
parser.add_argument("-o", metavar="output.pdf", help="Output filename")
args = parser.parse_args()

RE_PAGES = re.compile(r":(?P<lo>-?\d*):(?P<hi>-?\d*)$")

def maybe_int(s):
    return int(s) if s else None

def load_pages(ranges):
    for path in ranges:
        lo, hi = None, None
        m = RE_PAGES.search(path)
        if m:
            path = path[:m.start()]
            lo = maybe_int(m.group("lo"))
            hi = maybe_int(m.group("hi"))
        files = sorted(glob.glob(path))[lo:hi]
        yield from files

def interleave(items):
    for t in zip(*items):
        yield from t 

# Hard code the layout function to A4 atm
a4inpt = (img2pdf.mm_to_pt(210),img2pdf.mm_to_pt(297))
layout_fun = img2pdf.get_layout_fun(a4inpt)

sources = [load_pages(s) for s in args.s]
pages = list(interleave(sources))
with open(args.o, "wb") as f:
    f.write(img2pdf.convert(pages, layout_fun=layout_fun))
