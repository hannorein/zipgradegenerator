#!/usr/bin/env python3
import glob
import subprocess
import csv
from multiprocessing import Process,Manager
from checkSubmission import checkSubmission

def getStudentData(sid):
    with open('PSCB57H3-2016-F.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            if sid==row[0]:
                return row
    return [0000000000, "Name Not Found", "", "", "", "", "", "", "", "", "", ""]
    
with open('PSCB57H3-2016-F.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    with open('finalresult.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            sid = row[0]
            if sid=="StudentID":
                continue
            found = 0
            with open('quiz.csv', 'r') as csvfile2:
                reader2 = csv.reader(csvfile2, delimiter=',', quotechar='"')
                for row2 in reader2:
                    if row2[0]==sid:
                        quest = row2
                        found =1
            if found==0:
                print("Quiz questions not found")
            found = 0
            with open('quizDatafull.csv', 'r') as csvfile3:
                reader2 = csv.reader(csvfile3, delimiter=',', quotechar='"')
                for row2 in reader2:
                    if row2[5]==sid:
                        answ = row2
                        found =1
            if found==1:
                errors = 0
                for i in range(49):
                    ticked = 0
                    if answ[11+4*i]=="A":
                        ticked = 1
                    if ticked!=int(quest[8+i]):
                        errors += 1
                if answ[11+4*50]!="C":
                    errors += 1
                if answ[11+4*51]!="C":
                    errors += 1
                writer.writerow([sid, errors])
            else:
                # Quiz not found
                writer.writerow([sid, 99])


