#!/usr/bin/env python3
import glob
from pdfrw import PdfReader, PdfWriter, PageMerge
import subprocess
from shutil import copyfile
from generatezip import  getzipwithstudentid
import csv
import os

def getBugs(name):
    maxlines = 50
    f = "submissions/"+name
    fm = "submissions_with_bugs/"+name
    output = subprocess.Popen(["diff", "--unchanged-line-format=", "--old-line-format=","--new-line-format=%dn:", f, fm], stdout=subprocess.PIPE).communicate()[0].decode("ascii")
    with open(fm, 'r') as cf:
        fml = cf.read().splitlines()
    bugs = []
    for d in output.split(":"):
        if len(d):
            bugs.append(int(d))
    lines = []
    totalbugs = 0
    for i in range(len(fml)):
        if i in bugs:
            lines.append(1)
            totalbugs+=1
        else:
            lines.append(0)
    while len(lines)<maxlines:
        lines.append(0)
    return lines, totalbugs

for f in glob.glob("printouts/*.pdf"):
    os.remove(f)


with open('quiz.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"')
    with open('checked.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            if "1"==row[1]:
                f = row[5].split("/")[1]
                lines, totalbugs = getBugs(f)
                row.append(str(totalbugs))
                row = row + [str(i) for i in lines]
                writer.writerow(row)
                print(", ".join(row[0:3]+row[5:]))
                f = row[5]
                sid = f.split("/")[1].split(" ")[0]
                fm = "submissions_with_bugs/"+f.split("/")[1]
                copyfile(fm,"tmp.py")
                subprocess.Popen(["/Library/TeX/texbin/pdflatex", "source.tex"], stdout=subprocess.PIPE).communicate()[0]
                getzipwithstudentid("zipwithid.pdf",sid[1:])

                pdfwriter = PdfWriter()
                pdfwriter.addpages(PdfReader("source.pdf").pages)
                pdfwriter.addpages(PdfReader("zipwithid.pdf").pages)
                pdfwriter.write("printouts/quiz_"+sid+".pdf")

            else:
                print("Test not passed")

