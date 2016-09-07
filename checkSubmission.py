#!/usr/bin/env python3
import sys
import subprocess
import os
import signal
from multiprocessing import Process,Manager

correct_output = """1
1
3
5
13
21
55
89
233
377
"""

def runStudentCode(filename,return_dict):
    p = subprocess.Popen(["python3", filename], stdout=subprocess.PIPE,stderr=subprocess.STDOUT,preexec_fn=os.setpgrp)
    return_dict["pid"] = p.pid
    return_dict["output"] = p.communicate()[0].decode("ascii")

manager = Manager()
return_dict = manager.dict()

def checkSubmission(f):
    notcorrect = None
    if "output" in return_dict:
        del return_dict["output"]
    with open(f, 'r') as cf:
        sf = cf.read()
    if "import" in sf:
        notcorrect = "Import statement used"
    if "input" in sf:
        notcorrect = "Input statement used. Do not use the input statement for this assignment."
    if "377" in sf:
        notcorrect = "Fibonacci number hard coded"
    if "233" in sf:
        notcorrect = "Fibonacci number hard coded"
    if "89" in sf:
        notcorrect = "Fibonacci number hard coded"
    p = Process(target=runStudentCode,args=(f,return_dict))
    p.start()
    p.join(1)
    if p.is_alive():
        os.kill(-return_dict["pid"], signal.SIGTERM)
        notcorrect = "Runtime too long"
    if notcorrect is None:
        o = return_dict["output"]
        if o !=correct_output:
            if "SyntaxError" in o:
                notcorrect = "Syntax error"
            else:
                notcorrect = "Output not correct"
    return notcorrect

if __name__ == "__main__":
    if len(sys.argv)<2:
        print("This script checks assigments.\nUsage: checkSubmission.py FILENAME.py")
        exit(1)
    f = sys.argv[1]
    ret = checkSubmission(f)
    if ret:
        print("Test not passed. Reason:")
        print(checkSubmission(f))
    else:
        print("Test passed.")
