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
    
with open('checked.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"')
    for f in glob.glob("uploads/*.py"):
        sid = f.split("/")[1].split("_")[0]
        ret = checkSubmission(f)
        if ret is None:
            ok = "1"
            ret = "All ok"
        else:
            ok = "0"

        data = getStudentData(sid)
        row = [sid,ok,ret,data[1],data[11],f]
        print(", ".join(row))
        writer.writerow(row)

print("\nNo submission from:\n")

with open('PSCB57H3-2016-F.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    emails=""
    with open('checked_sorted.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            sid = row[0]
            if sid=="StudentID":
                continue
            found = 0
            with open('checked.csv', 'r') as csvfile2:
                reader2 = csv.reader(csvfile2, delimiter=',', quotechar='"')
                for row2 in reader2:
                    if row2[0]==sid:
                        writer.writerow(row2)
                        found =1
            if found==0:
                print(row)
                data = getStudentData(sid)
                writer.writerow([sid,"0","No submission",data[1],data[11],""])
                emails += row[-1]+", "

print("\n"+emails[:-2])


print("\nSubmissions from students not enrolled:\n")
with open('checked.csv', 'r') as csvfile2:
    reader2 = csv.reader(csvfile2, delimiter=',', quotechar='"')
    emails=""
    for row in reader2:
        sid = row[0]
        found = 0
        with open('PSCB57H3-2016-F.csv', 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='"')
            for row2 in reader:
                if row2[0]==sid:
                    found =1
        if found==0:
            print(row)
