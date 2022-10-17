#!/usr/bin/env python
import argparse
from bracket import Bracket
from backtrack import Backtrack
import sys
import subprocess
import os
import numpy as np

def ferror(WORK_DIR,CURRENT_DIR):
    """ Return Misfit Value """

    os.chdir(WORK_DIR)
    step = float(np.loadtxt(CURRENT_DIR+"/alpha"))
    command="workflow_py_update_model.sh PAR_INV {} 1".format(str(step))
    print ("running : ",command)
    subprocess.run(command,shell=True,check=True)
    command="workflow_py_eval_misfit.sh PAR_INV 1"
    os.chdir(WORK_DIR)
    print ("running : ",command)
    subprocess.run(command,shell=True,check=True)
    fval =float(np.loadtxt(CURRENT_DIR+"/fval"))
    os.chdir(CURRENT_DIR)
    return fval


parser=argparse.ArgumentParser(description="Line search")
parser.add_argument('-workdir',type=str,required=True)
parser.add_argument('-funcval',type=float,required=True)
parser.add_argument('-funcval_old',type=float,default=0.0)
parser.add_argument('-step',type=float,default=0.0)
parser.add_argument('-step_old',type=float)
parser.add_argument('-step_max',type=float,required=True)
parser.add_argument('-gtg',type=float,required=True)
parser.add_argument('-gtp',type=float,required=True)
parser.add_argument('-gtp_old',type=float,default=None)
parser.add_argument('-step_trials',type=int,default=3)
parser.add_argument('-linesearch',type=str,default="bracket")



args=parser.parse_args()

print(args)


if (args.linesearch == "bracket"):
    print ("Line search: ",args.linesearch)
    line_search=Bracket(step_count_max=args.step_trials,step_len_max=args.step_max,path="./steps")

elif (args.linesearch == "backtrack"):
    print ("Line search: ",args.linesearch)
    line_search=Backtrack(step_count_max=args.step_trials,step_len_max=args.step_max,path="./steps")

if args.step_old:
    line_search.step_lens += [args.step_old]
    line_search.func_vals += [args.funcval_old]
    line_search.gtp += [args.gtp_old]
    line_search.count_zeros=1
        

WORK_DIR=args.workdir
CURRENT_DIR=os.getcwd()

alpha,status =line_search.initialize(step_len=args.step,
                       func_val=args.funcval,
                       gtg=args.gtg,
                       gtp=args.gtp)


f=open("alpha","w")
f.write("%.4e" % (alpha))
f.close()
    
f=open("status","w")
f.write("%d" % (status))
f.close()


while status== 0:
    alpha,status = line_search.update(alpha,ferror(WORK_DIR,CURRENT_DIR))

    print(alpha,status)

    f=open("alpha","w")
    f.write("%.4e" % (alpha))
    f.close()
    
    f=open("status","w")
    f.write("%d" % (status))
    f.close()
    
    if (status < 0):
        sys.exit(1)
        break

    








