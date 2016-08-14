#!/usr/bin/env python3
import sys
import subprocess
from multiprocessing import Process,Manager

def runStudentCode(filename,return_dict):
    output = subprocess.Popen(["python3", filename], stdout=subprocess.PIPE,stderr=subprocess.STDOUT).communicate()[0].decode("ascii")
    return_dict["output"] = output

with open('correct_output.txt', 'r') as cf:
    correct_output = cf.read()

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
    p = Process(target=runStudentCode,args=(f,return_dict))
    p.start()
    p.join()
    if notcorrect is None:
        if return_dict["output"]!=correct_output:
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
