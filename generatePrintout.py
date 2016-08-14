#!/usr/bin/env python3
import glob
from pdfrw import PdfReader, PdfWriter, PageMerge
import subprocess
from shutil import copyfile
from generatezip import  getzipwithstudentid
import csv

with open('checked.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        print("Generating file for " + row[3])
        if "1"==row[1]:
            print("Test passed")
            f = row[5]
            sid = f.split("/")[1].split(" ")[0]
            fm = "submissions_with_bugs/"+f.split("/")[1]
            copyfile(fm,"tmp.py")
            subprocess.Popen(["/Library/TeX/texbin/pdflatex", "source.tex"], stdout=subprocess.PIPE).communicate()[0]
            getzipwithstudentid("zipwithid.pdf",sid[1:])

            writer = PdfWriter()
            writer.addpages(PdfReader("source.pdf").pages)
            writer.addpages(PdfReader("zipwithid.pdf").pages)
            writer.write("printouts/quiz_"+sid+".pdf")

        else:
            print("Test not passed")

