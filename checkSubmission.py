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
    if "lsf" not in dir(pm):
        if "lst" not in dir(pm):
            return "Function lsf(x,y,t) not defined."
        pm.lsf = pm.lst


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

    sol =  pm.s(A,v)
    if len(sol) != len(v):
        return "Incorrect dimensions in return value from s()."
    for i in range(len(sol)):
        if abs( (sol[i]-sol1[i]) / sol1[i])>1e-5:
            return "Function s() does not seem to solve a linear system of equations correctly."
    
    
    ############
    ############  Test for lsf()
    ############
    def ft(x):
        return [1.,x]

    x = [0.,1.,2.,3.]
    y = [1.,2.,3.,4.]
    sol1 = [1.,1.]

    sol =  pm.lsf(x,y,ft)
    M = len(ft(x[0]))
    if len(sol) != M:
        return "Incorrect dimensions in return value from lsf()."
    for i in range(len(sol)):
        if abs( (sol[i]-sol1[i]) / sol1[i])>1e-5:
            return "Function sf) does not seem to solve a linear system of equations correctly."
    

    x = [1980 , 1981 , 1982 , 1983 , 1984 , 1985 , 1986 , 1987 , 1988 , 1989 , 1990 , 1991 , 1992 , 1993 , 1994 , 1995 , 1996 , 1997 , 1998 , 1999 , 2000 , 2001 , 2002 , 2003 , 2004 , 2005 , 2006 , 2007 , 2008 , 2009 , 2010 , 2011 , 2012 , 2013 , 2014]
    y = [ 0.135, 0.317, -0.002, 0.331, -0.045, -0.033, 0.120, 0.252, 0.375, 0.245, 0.492, 0.397, 0.093, 0.175, 0.343, 0.592, 0.227, 0.518, 0.835, 0.561, 0.484, 0.681, 0.778, 0.770, 0.674, 0.882, 0.810, 0.909, 0.695, 0.731, 0.901, 0.695, 0.751, 0.791, 0.762]
   
    sol1 = [-48.69734,0.024631]

    sol =  pm.lsf(x,y,ft)
    M = len(ft(x[0]))
    if len(sol) != M:
        return "Incorrect dimensions in return value from lsf()."
    for i in range(len(sol)):
        if abs( (sol[i]-sol1[i]) / sol1[i])>1e-4:
            return "Function lsf() does not seem to o the fit correctly."
    

    def ft(x):
        return [1.,x, x*x]
    
    sol1 = [-1015.407,0.992819,-0.000242410]

    sol =  pm.lsf(x,y,ft)
    M = len(ft(x[0]))
    if len(sol) != M:
        return "Incorrect dimensions in return value from lsf()."
    for i in range(len(sol)):
        if abs( (sol[i]-sol1[i]) / sol1[i])>1e-4:
            return "Function lsf() does not seem to o the fit correctly."
    



    
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
