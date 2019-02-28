#!/usr/bin/env python

# Author: Sebastian Lee (sjrl423@gmail.com)
# Composed: 08-18-16
# Description: Python script to check if the jobs succesfully completed in Molpro
#
# Input parameters
#   dir_name     (type: string)  --> The directory path you would like to start the program


import os
import sys
import fnmatch

def file_check(dir_name,print_info):

    list_of_success = []
    list_of_failure = []
    run_dict = {}

    cwd = os.getcwd()

    # A bit of a hack such that if the symbol '.' is passed at the command line for this script
    # then it knows to start cleaning from the current working directory.
    if dir_name == '.':
        dir_name = './'

    for dirpath, dirs, filenames in os.walk(dir_name):
        for filename in filenames:

            # Check to see if there is a batch file present.
            # This means a job is meant to be run in this folder.
            if filename[-5:] == 'batch':

                run_dict[dirpath] = filename

                files = [f for f in os.listdir(dirpath) if os.path.isfile(os.path.join(dirpath,f))]

                # Determine if a job has already been run
                job_was_run = False
                for f in files:
                    if fnmatch.fnmatch(f,'job*out'):
                        job_was_run = True
                        del run_dict[dirpath]

                # Check for output files if the job was run
                if job_was_run:

                    output_detected=False

                    for f in files:
                        # For molpro jobs
                        if f[-3:] == 'out' and f[:3] != 'job':

                            output_detected=True

                            # "with" places the opened object into file1 for use in the nested block of commmands
                            with open(os.path.join(dirpath,f),'r') as file1:

                                # NOTE: python's open creates a line by line iterator in the constructor of the file object
                                # This loop passes every line. The last value of lines will the be the last line in the file.
                                for lc,lines in enumerate(file1):
                                    pass

                                lastFields = lines.split()
                                if len(lastFields) == 3 and lastFields[0] == "Variable" and lastFields[1] == "memory" and lastFields[2] == "released":
                                    #list_of_success.append(lastFolder)
                                    list_of_success.append(dirpath)
                                elif len(lastFields) >= 3 and lastFields[0] == "Molpro" and lastFields[1] == "calculation" and lastFields[2] == "terminated":
                                    #list_of_success.append(lastFolder)
                                    list_of_success.append(dirpath)
                                else:
                                    #list_of_failure.append(lastFolder)
                                    list_of_failure.append(dirpath)

                        # For geometric jobs
                        elif f == 'progress.txt':

                            output_detected=True

                            # "with" places the opened object into file1 for use in the nested block of commmands
                            with open(os.path.join(dirpath,f),'r') as file1:

                                # This loop passes every line. The last value of lines will the be the last line in the file.
                                for lc,lines in enumerate(file1):
                                    pass

                                lastFields = lines.split()
                                if lastFields[0] == 'Converged!':
                                    #list_of_success.append(lastFolder)
                                    list_of_success.append(dirpath)
                                else:
                                    #list_of_failure.append(lastFolder)
                                    list_of_failure.append(dirpath)
                    if not output_detected:
                        # No output files detected
                            list_of_failure.append(dirpath)

    if (print_info):
        # Print info about the different states of the jobs
        print('\n'+cwd+'\n')

        # Print amount of successful jobs
        print('List of Success:')
        if len(list_of_success) > 100:
            print(str(len(list_of_success))+' jobs completed.')
        else:
            print(str(len(list_of_success))+' jobs completed.')
            print(list_of_success)
        print('')

        # Print amount of failed jobs
        print('List of Failure:')
        if len(list_of_failure) > 100:
            print(str(len(list_of_failure))+' jobs failed.')
        else:
            print(str(len(list_of_failure))+' jobs failed.')
            print(list_of_failure)
        print('')

        # Print jobs that still need to be submitted
        print('Jobs that need to be submitted:')
        if len(run_dict) > 100:
            print(str(len(run_dict))+' jobs need to be run.')
        else:
            print(str(len(run_dict))+' jobs need to be run.')
            print(run_dict)


    return list_of_success, list_of_failure, run_dict

if __name__ == "__main__":
    print_info=True
    file_check(sys.argv[1],print_info)
