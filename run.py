#!/usr/bin/env python

import os
import subprocess
import sys
sys.path.insert(0,'/home/sjlee/scripts/executableScripts')
from fchk import fileCheck


def runInput(run_dict):
    
    cwd = os.getcwd()
    for key in run_dict:
        # key should be full path
        os.chdir(os.path.join(cwd,key))
        cmd = ['sbatch',run_dict[key]]
        subprocess.Popen(cmd).wait()


if __name__ == "__main__":
    dir_name = sys.argv[1]
    print_info = False
    list_of_sucess, list_of_failure, run_dict = fileCheck(dir_name,print_info)
    runInput(run_dict)
    print( str(len(run_dict)) + ' jobs submitted.')
