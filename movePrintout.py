#!/usr/bin/env python3
import glob
from pdfrw import PdfReader, PdfWriter, PageMerge
import subprocess
from shutil import copyfile
from generatezip import  getzipwithstudentid
import csv
import os
import random

maxlines = 70

for f in glob.glob("printouts/*.pdf"):
    o = subprocess.Popen(["mdls", "-name", "kMDItemNumberOfPages", f], stdout=subprocess.PIPE).communicate()[0]
    n = int(o.split()[2])
    if (n>2):
        print("Moving " +f)
        os.rename(f,"printouts_3pages/"+f.split("/")[1])


