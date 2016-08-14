#!/usr/bin/env python3
import glob
import subprocess

for f in glob.glob("submissions/*.py"):
    sid = f.split("/")[1].split(" ")[0]
    fm = "submissions_with_bugs/"+f.split("/")[1]
    output = subprocess.Popen(["diff", "--unchanged-line-format=", "--old-line-format=","--new-line-format=%dn:", f, fm], stdout=subprocess.PIPE).communicate()[0].decode("ascii")
    with open(fm, 'r') as cf:
        fml = cf.read().splitlines()
    bugs = []
    for d in output.split(":"):
        if len(d):
            bugs.append(int(d))
    for i in range(len(fml)):
        isbug = 0
        if i in bugs:
            isbug =1
        print(i,isbug)



