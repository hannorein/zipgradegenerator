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

def getStudentData(sid):
    with open('PSCB57H3-2016-F.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            if sid==row[0]:
                return row
    return None

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
    for i in range(len(fml)+1):
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
alpha = ["A","B","C","D","E"]

with open('quiz.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"')
    with open('checked_sorted.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            if "1"==row[1]:
                f = row[5].split("/")[1]
                lines, totalbugs = getBugs(f)
                if totalbugs<1:
                    print("Warning. Not enough bugs.")
                row.append(str(totalbugs))
                row = row + [('A' if i==1 else '') for i in lines]
                sid = f[0:10]
                fm = "uploads_with_bugs/"+f
                copyfile(fm,"tmp.py")
                with open('q1.tex', 'w') as qf:
                    qf.write(" \\textbf{Question 71:}\\\\\n Suppose \\texttt{x} is a negative integer. What is \\texttt{f(x)}?   \\begin{multicols}{5}\\begin{itemize}")
                    answers = [ (0, " 0.0"),
                            (0, " -inf"),
                            (0, " inf"),
                            (1, " 1.0"),
                            (0, " nan") ]
                    random.shuffle(answers)
                    correctanswers = ""
                    for i, a in enumerate(answers):
                        rw , lt = a
                        qf.write("\\item[\\circled{"+alpha[i]+"}] ")
                        qf.write(lt+"\n")
                        if rw==1:
                            correctanswers += alpha[i]
                    qf.write(" \\end{itemize}\\end{multicols}")
                    row = row + [correctanswers]
                with open('q2.tex', 'w') as qf:
                    qf.write(" \\textbf{Question 72:}\\\\\n Mark all numbers which could be used in the \\texttt{range()} statement in the function \\texttt{g} and give the correct behaviour.  \\begin{multicols}{5}\\begin{itemize}")
                    answers = [ (0, " 16"),
                            (0, " 308"),
                            (1, " 700"),
                            (1, " 1024"),
                            (1, " 2048") ]
                    random.shuffle(answers)
                    correctanswers = ""
                    for i, a in enumerate(answers):
                        rw , lt = a
                        qf.write("\\item[\\circled{"+alpha[i]+"}] ")
                        qf.write(lt+"\n")
                        if rw==1:
                            correctanswers += alpha[i]
                    qf.write(" \\end{itemize}\\end{multicols}")
                    row = row + [correctanswers]
                with open('q3.tex', 'w') as qf:
                    qf.write(" \\textbf{Question 73:}\\\\\n What is the complexity of \\texttt{fib2(n)} for large \\texttt{n}?   \\begin{multicols}{5}\\begin{itemize}")
                    answers = [ (0, "$O(1)$"),
                            (0, " $O(n)$"),
                            (1, " $O(\log(n))$"),
                            (0, " $O(n^2)$"),
                            (0, " $O(2^n)$") ]
                    random.shuffle(answers)
                    correctanswers = ""
                    for i, a in enumerate(answers):
                        rw , lt = a
                        qf.write("\\item[\\circled{"+alpha[i]+"}] ")
                        qf.write(lt+"\n")
                        if rw==1:
                            correctanswers += alpha[i]
                    qf.write(" \\end{itemize}\\end{multicols}")
                    row = row + [correctanswers]
                with open('q4.tex', 'w') as qf:
                    qf.write(" \\textbf{Question 74:}\\\\\n Which of the algorithms returns the exact Fibonacci number for $n=89$?   \\begin{multicols}{5}\\begin{itemize}")
                    answers = [ 
                            (0, "\\texttt{fib1(n)}"),
                            (1, "\\texttt{fib2(n)}"),
                            (0, "\\texttt{fibd(n)}"),
                            (0, "none"),
                            (0, "\\texttt{f(n)}"),
                             ]
                    random.shuffle(answers)
                    correctanswers = ""
                    for i, a in enumerate(answers):
                        rw , lt = a
                        qf.write("\\item[\\circled{"+alpha[i]+"}] ")
                        qf.write(lt+"\n")
                        if rw==1:
                            correctanswers += alpha[i]
                    qf.write(" \\end{itemize}\\end{multicols}")
                    row = row + [correctanswers]
                with open('name.tex', 'w') as the_file:
                    the_file.write(row[3])
                with open('studentnumber.tex', 'w') as the_file:
                    for s in sid[1:]:
                        the_file.write(s+"\\hspace{3.6mm}")
                subprocess.Popen(["/Library/TeX/texbin/pdflatex", "source.tex"], stdout=subprocess.PIPE).communicate()[0]
                subprocess.Popen(["/Library/TeX/texbin/pdflatex", "source2.tex"], stdout=subprocess.PIPE).communicate()[0]
                getzipwithstudentid("zipwithid.pdf",sid[1:])
                
                print(", ".join(row[0:3]+row[6:]))

                pdfwriter = PdfWriter()
                pdfwriter.addpages(PdfReader("zipwithid.pdf").pages)
                pdfwriter.addpages(PdfReader("source.pdf").pages)
                try:
                    tut = getStudentData(sid)[5]
                except:
                    tut = "NOTFOUND"
                pdfwriter.write("printouts/quiz_"+tut+"_"+sid+".pdf")
                #exit(0)
            else:
                row = row + ["0" for i in range(maxlines+1)]
                print(", ".join(row[0:3]+["Test not passed"]))
            writer.writerow(row)


