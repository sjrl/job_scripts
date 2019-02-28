#!/usr/bin/env python

# Author: Sebastian Lee (sjrl423@gmail.com)
# Composed: 02-02-17
# Description: Python script to check if the jobs succesfully completed in Molpro
#
# Input parameters
#   dirname     (type: string)  --> The directory path you would like to start the program


import argparse
import os
import subprocess
import sys
from fchk import file_check


# FIXME Needs to be modified to be able to delete folders I specify as well
def jclean(**kwargs):

    recursive = kwargs.get('r', False)
    failed_jobs = kwargs.get('failed', False)
    path = kwargs.get('path')
    files_to_delete = kwargs.get('filenames')
    folders_to_delete = kwargs.get('folders',None)

    # Create directory path for os.walk to start at
    dir_name = os.path.join(os.getcwd(),path)

    # Recursively clean directories
    if recursive:
        for dirpath, dirs, filenames in os.walk(dir_name):
            for filename in filenames:

                # Resets save logical for every new filename
                save = True

                # Checks if any of the strings in files_to_delete exist in filename.
                # And if any of the strings do the save logical is set to False
                # and the for loop is broken (it only needs to be recognized once).
                for item in files_to_delete:
                    if item in filename:
                        save = False
                        break

                # For debugging. Checking that save flag is changed properly.
                #print(str(save)+': '+filename)

                # If the save flag is still False then the file called filename is removed.
                if not save:
                    os.chdir(dirpath)
                    subprocess.call(["rm"] + [filename])

    # Clean only failed jobs starting at current directory or specified directory from path
    elif failed_jobs:
        print_info = False
        list_of_sucess, list_of_failure, run_dict = file_check(dir_name,print_info)

        if len(list_of_failure) == 0:
            print('0 failed jobs detected.')

        for dir_fail in list_of_failure:
            # gather files in directory dir_fail
            files = [f for f in os.listdir(dir_fail) if os.path.isfile(os.path.join(dir_fail,f))]

            for filename in files:
                # Determine which files to be saved
                save = True
                for item in files_to_delete:
                    if item in filename:
                        save = False
                        break
                # Delete files that aren't saved
                if not save:
                    os.chdir(dir_fail)
                    subprocess.call(["rm"] + [filename])
            
            if folders_to_delete is not None:
                # gather dirs in directory dir_fail
                folders = [fold for fold in os.listdir(dir_fail) if os.path.isdir(os.path.join(dir_fail,fold))]
                for folder_name in folders:
                    # Determine which folders to be saved
                    save = True
                    for item in folders_to_delete:
                        if item == folder_name:
                            save = False
                            break
                    # Delete folders that aren't saved
                    if not save:
                        os.chdir(dir_fail)
                        subprocess.call(["rm","-r",folder_name])
        
        print(str(len(list_of_failure))+' failed jobs cleaned.')
            
    # Default behavior, clean current directory or specified directory from path
    else:
        # Gather files in directory dir_name
        files = [f for f in os.listdir(dir_name) if os.path.isfile(os.path.join(dir_name,f))]

        for filename in files:
            # Determine which files to be saved
            save = True
            for item in files_to_delete:
                if item in filename:
                    save = False
                    break
            # Delete files that aren't saved
            if not save:
                os.chdir(dir_name)
                subprocess.call(["rm"] + [filename])

        if folders_to_delete is not None:
            # gather dirs in directory dir_name
            folders = [fold for fold in os.listdir(dir_name) if os.path.isdir(os.path.join(dir_name,fold))]
            for folder_name in folders:
                # Determine which folders to be saved
                save = True
                for item in folders_to_delete:
                    if item == folder_name:
                        save = False
                        break
                # Delete folders that aren't saved
                if not save:
                    os.chdir(dir_name)
                    subprocess.call(["rm","-r",folder_name])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--filenames', type=str, nargs='+', required=False, help='Specify the file types to be deleted.')
    parser.add_argument('--path', type=str, default=os.getcwd(), help='Specify path to begin cleaning from.')
    parser.add_argument('--r', action='store_true', help='Clean all folders recursively starting at PATH or current working directory (as default).')
    parser.add_argument('--failed', action='store_true', help='Clean all failed jobs.')
    parser.add_argument('--folders', type=str, nargs='+', help='Specify the folders to be deleted.')
    args = parser.parse_args(sys.argv[1:])

    jclean(**vars(args))
