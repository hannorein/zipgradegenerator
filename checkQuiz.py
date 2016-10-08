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
                print(sid, "Quiz questions not found")
            if found==1 and quest[1]=="0":
                print(sid, "Assignment not correct")
                writer.writerow([sid, 99])
                continue
            found = 0
            with open('quizDatafull.csv', 'r') as csvfile3:
                reader2 = csv.reader(csvfile3, delimiter=',', quotechar='"')
                for row2 in reader2:
                    if row2[5]==sid:
                        answ = row2
                        found =1
            if found==0:
                print(sid, "Quiz answers not found")
                writer.writerow([sid, 99])
                continue
            errors = 0
            errorsquest = 0
            for i in range(74):
                if i==68 or i == 69:
                    continue
                if i<69:
                    quickfix = 1
                else:
                    quickfix = 0
                #if sid == "1000186924":
                #    print(i+1,"q",quest[7+i+quickfix],"a",answ[11+4*i],"e")
                if answ[11+4*i]!=quest[7+i+quickfix]:
                    errors += 1
                    if i>70:
                        errorsquest +=1
            #print(sid,"Errors:", errors, "\t\t", errorsquest+min(1,errors-errorsquest))
            print(sid,"Errors:", errorsquest,  errorsquest+min(1,errors-errorsquest))
            writer.writerow([sid, errorsquest+min(1,errors-errorsquest)])


