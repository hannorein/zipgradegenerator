#!/usr/bin/env python3
import glob
from pdfrw import PdfReader, PdfWriter, PageMerge
import subprocess
from shutil import copyfile
from generatezip import  getzipwithstudentid
import csv
import os

maxlines = 50

def getBugs(name):
    f = "uploads/"+name
    fm = "uploads_with_bugs/"+name
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
            f = row[5].split("/")[1]
            if "1"==row[1]:
                lines, totalbugs = getBugs(f)
                if totalbugs<1:
                    print("Warning. Not enough bugs.")
                row.append(str(totalbugs))
                row = row + [str(i) for i in lines]
                print(", ".join(row[0:3]+row[6:]))
                sid = f[0:10]
                fm = "uploads_with_bugs/"+f
                copyfile(fm,"tmp.py")
                subprocess.Popen(["/Library/TeX/texbin/pdflatex", "source.tex"], stdout=subprocess.PIPE).communicate()[0]
                with open('name.tex', 'w') as the_file:
                    the_file.write(row[3])
                with open('studentnumber.tex', 'w') as the_file:
                    for s in sid[1:]:
                        the_file.write(s+"\\hspace{3.6mm}")
                subprocess.Popen(["/Library/TeX/texbin/pdflatex", "source2.tex"], stdout=subprocess.PIPE).communicate()[0]
                getzipwithstudentid("zipwithid.pdf",sid[1:])

                pdfwriter = PdfWriter()
                pdfwriter.addpages(PdfReader("source.pdf").pages)
                pdfwriter.addpages(PdfReader("zipwithid.pdf").pages)
                pdfwriter.write("printouts/quiz_"+sid+".pdf")
            else:
                row = row + ["0" for i in range(maxlines+1)]
                print(", ".join(row[0:3]+["Test not passed"]))
            writer.writerow(row)

