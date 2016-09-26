#!/usr/bin/env python3
import sys
import subprocess
import os
from os.path import basename, splitext
import signal
import inspect
import math
sys.path.insert(0, "./uploads")
from multiprocessing import Process,Manager

correct_output = """"""

def runStudentCode(filename,return_dict):
    p = subprocess.Popen(["python3", filename], stdout=subprocess.PIPE,stderr=subprocess.STDOUT,preexec_fn=os.setpgrp)
    return_dict["pid"] = p.pid
    return_dict["output"] = p.communicate()[0].decode("ascii")

manager = Manager()
return_dict = manager.dict()

def checkSubmission(f):
    if "output" in return_dict:
        del return_dict["output"]
    with open(f, 'r') as cf:
        sf = cf.readlines()
    if len(sf)>70:
        return "Too many lines of code (max: 70)."
    for l in sf:
        if "import" in l:
            if l.strip() != "from numpy.linalg import solve":
                return "You may only use the following import statement: from numpy.linalg import solve"
    with open(f, 'r') as cf:
        sf = cf.read()
    if "input" in sf:
        return "Input statement used. Do not use the input statement for this assignment."
    pm = __import__(splitext(basename(f))[0])
    if "s" not in dir(pm):
        return "Function s(A,v) not defined."
    if "lst" not in dir(pm):
        return "Function lst(x,y,t) not defined."


    ############
    ############  Test for s()
    ############
    A = [[2.,  1.,  4.,  1.],
         [3.,  4., -1., -1.],
         [1., -4.,  1.,  5.],
         [2., -2.,  1.,  3.]]

    v = [-4., 3., 9., 7. ]
    sol1 = [ 2., -1., -2.,  1.]

    try:
        sol =  pm.s(A,v)
        if len(sol) != len(v):
            return "Incorrect dimensions in return value from s()."
        for i in range(len(sol)):
            if abs( (sol[i]-sol1[i]) / sol1[i])>1e-8:
                return "Function s() does not seem to solve a linear system of equations correctly."
    except:
        return "Something went wrong when executing the function s() to solve a linear system of equations."
    
    
    ############
    ############  Test for s()
    ############
    A = [[0.,  1.,  4.,  1.],
         [3.,  4., -1., -1.],
         [1., -4.,  1.,  5.],
         [2., -2.,  1.,  3.]]

    v = [-4., 3., 9., 7. ]
    sol1 =[ 1.61904762, -0.42857143, -1.23809524,  1.38095238]

    try:
        sol =  pm.s(A,v)
        if len(sol) != len(v):
            return "Incorrect dimensions in return value from s()."
        for i in range(len(sol)):
            if abs( (sol[i]-sol1[i]) / sol1[i])>1e-5:
                return "Function s() does not seem to solve a linear system of equations correctly."
    except:
        return "Something went wrong when executing the function s() to solve a linear system of equations."
    
    


    
    p = Process(target=runStudentCode,args=(f,return_dict))
    p.start()
    p.join(1)
    if p.is_alive():
        os.kill(-return_dict["pid"], signal.SIGTERM)
        return "Runtime too long"
    o = return_dict["output"]
    if o !=correct_output:
        if "SyntaxError" in o:
            return "Syntax error"
        else:
            return "Output not correct"
    return None

if __name__ == "__main__":
    if len(sys.argv)<2:
        print("This script checks assigments.\nUsage: checkSubmission.py FILENAME.py")
        exit(1)
    f = sys.argv[1]
    ret = checkSubmission(f)
    if ret:
        print("Test not passed. Reason:")
        print(ret)
    else:
        print("Test passed.")
