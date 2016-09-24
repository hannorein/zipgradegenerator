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
    with open(f, 'r') as cf:
        sf = cf.read()
    if "import" in sf:
        return "Import statement used"
    if "input" in sf:
        return "Input statement used. Do not use the input statement for this assignment."
    pm = __import__(splitext(basename(f))[0])
    if "f" not in dir(pm):
        return "Function f not defined."
    if "g" not in dir(pm):
        return "Function g not defined."


    ############
    ############  Test for f(x)
    ############
    flines,flinesn = inspect.getsourcelines(pm.f)
    allowedchars = ["d","e","f"," ","(","x",")",":","\n","r","t","u","n","\t","1","-","+","/"]
    for l in flines:
        for c in l:
            if c not in allowedchars:
                return "Character not allowed: '"+c+"'."
    
    corf = [[1e-16, 0.], [ 2.5e-16,1.],[1e-13,0.9988901220865705],[1.12e-16,2.],[-1e15,1.],[1e-15,1.1111111111111112]]
    for a,b in corf:
        try:
            if pm.f(a)!=b:
                return "Incorrect return value for f(%.16e)."%a
        except:
            return "Incorrect return value for f(%.16e)."%a
    
    ############
    ############  Test for g(x)
    ############
    glines,glinesn = inspect.getsourcelines(pm.g)
    ffor = 0
    for l in glines:
        if "for" in l:
            ffor = 1
    if ffor==0:
        return "Function g contains no for loop."


    corg = [[1e-300, float("inf")], [0.,0.],[0,0],[-1e-15,float("-inf")],[1e300,float("inf")]]
    for a,b in corg:
        try:
            if pm.g(a)!=b:
                return "Incorrect return value for g(%.16e)."%a
        except:
            return "Incorrect return value for g(%.16e)."%a
            pass

    
    for a in [0,1,1000000,2000,-234234,10000002030403827287872]:
        try:
            if math.isinf(pm.g(a)):
                return "Incorrect return value for g(%d)."%a
        except OverflowError:
            pass
        except:
            return "Incorrect return value for g(%d)."%a
            pass
    
    ############
    ############  Test for fibd(x)
    ############
    corfibd = [[1,0.], [10,1.421085471520200372e-14],[20,4.547473508864641190e-12]]
    for a,b in corfibd:
        try:
            if math.fabs(pm.fibd(a)-b)>max(1e-10,1e-10*b):
                return "Incorrect return value for fibd(%d)."%a
        except:
            return "Incorrect return value for fibd(%d)."%a
            pass
    try:
        if math.fabs(pm.fibd(90))<1000:
            return "Incorrect return value for fibd(%d)."%90
    except:
        return "Incorrect return value for fibd(%d)."%90


    
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
