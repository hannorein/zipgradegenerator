#!/usr/bin/env python3
import glob
import subprocess
import csv
from multiprocessing import Process,Manager
from checkSubmission import checkSubmission

def getStudentData(sid):
    with open('PSCB57H3-2016-F-2.csv', 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='"')
        for row in reader:
            if sid==row[0]:
                return row
    
with open('checked.csv', 'w') as csvfile:
    writer = csv.writer(csvfile, delimiter=',', quotechar='"')
    for f in glob.glob("submissions/*.py"):
        sid = f.split("/")[1].split(" ")[0]
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


