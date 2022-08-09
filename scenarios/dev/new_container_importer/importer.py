#! /usr/bin/python
import fileinput
import sys
from os.path import exists
import os
from pathlib import Path
import re as re
import shutil as shutil

# Variables which might require maintenance in the future
MIN_PYTHON = (3, 8) # Python 3.8
ENV_PATH = "..\..\.."
ENV_NAME = ".env"
ENV_SCENARIO_VARNAME = "SCENARIO_LIST_ENV"
BANNEDCHARS = [ "/", " ", "\'", "\"", "*", ">", "<", "=", "+", ";", "&", "\n", '\\', "\r", "$", "!", "|"]
PROD_RELATIVE_PATH = "..\..\prod"
DEV_RELATIVE_PATH = "..\..\dev"
cwd = Path(__file__).parent

def getEnvString():
    # Make sure the .env file exists, is a file, we can read it, and we can write to it.
    tPath = (cwd / ENV_PATH).resolve()
    filepath = ((str(tPath) + "\\") + ENV_NAME)
    retVal = ""
    if not (exists(filepath) & os.path.isfile(filepath) & os.access(filepath, os.R_OK) & os.access(filepath, os.W_OK)):
        print("Path specified: %s" % filepath)
        sys.exit("The .env file could not be located, read, or written to. Check that the .env file exists, and that you have permissions to read and write to it.\n")
    handle = open(filepath, "r")
    for line in handle:
        if (line.startswith(ENV_SCENARIO_VARNAME)):
            retVal = line
    handle.close()
    if not retVal:
        sys.exit("Scenario variable could not be located.\n")
    return retVal

def WriteEnvString(inputStr: str, shortEnv: str):
    newEnvVar = ENV_SCENARIO_VARNAME+"=\'"+shortEnv+','+"\""+inputStr+"\""+"\'"
    tPath = (cwd / ENV_PATH).resolve()
    filepath = (tPath / ENV_NAME).resolve()
    for line in fileinput.input(filepath, inplace=1):
        line = line.replace(envVarStr, newEnvVar)
        sys.stdout.write(line)

def GetScenarioName(name: str):
    entry = name
    # Check for illegal characters
    i = 0
    while i < len(BANNEDCHARS):
        if re.search(re.escape(BANNEDCHARS[i]), entry):
            sys.exit(f"Scenario name contains a banned character.\n Don't use {' '.join(BANNEDCHARS)}, \\, space, CR, LF")
        i = i + 1
    return entry

if __name__== "__main__":
    # Check the python version. From https://stackoverflow.com/a/34911547
    if sys.version_info < MIN_PYTHON:
        sys.exit("Python %s.%s or later is required.\n" % MIN_PYTHON)

    # Get the env file variable first and check that it is formatted properly
    envVarStr = getEnvString()

    # Remove the start of the string. Replace it later.
    replace = ENV_SCENARIO_VARNAME + "="
    shortEnv = envVarStr.replace(replace, "") 

    # Make sure the variable is wrapped with single quotes.
    if not (shortEnv.startswith("\'") & shortEnv.endswith("\'")):
        print(shortEnv)
        sys.exit("Improperly formatted scenario variable in .env file.\n")
    else:
        shortEnv = shortEnv.lstrip('\'')
        shortEnv = shortEnv.rstrip('\'')
    if len(sys.argv) != 2:
        print("Usage: importer.py SCENARIO_NAME")
        print("Where scenario name is the name of the folder which contains the scenario files.")    
        sys.exit()

    scenarioName = GetScenarioName(str(sys.argv[1]))

    #Check to see if the scenario already exists in prod directory. If it does, abort.
    prodRelPath = (cwd / PROD_RELATIVE_PATH).resolve()
    prodScen = (prodRelPath / scenarioName).resolve()
    if(exists(prodScen)):
        sys.exit("The name of this scenario already exists in the prod directory. Please choose a different name.\n")
    
    # Check for if the name requested is already in the ENV list of names
    testScenName = '\'' + scenarioName + '\''
    if testScenName in shortEnv.split(","):
        sys.exit("Scenario name is already used. Please check this list and make sure your name does not conflict.\n %s\n", shortEnv)

    # Copy files from /dev to /prod
    # First, check to see that the folder is in /dev
    devRelPath = (cwd / DEV_RELATIVE_PATH).resolve()
    devScen = (devRelPath / scenarioName).resolve()
    if(not exists(devScen)):
        sys.exit("Could not locate folder %s in %s.\n", scenarioName, devRelPath)
    shutil.copytree(devScen, prodScen, ignore=None, dirs_exist_ok=False)

    # Write the .env string
    WriteEnvString(scenarioName, shortEnv)

    # Exit
    print("Finished importing scenario files.\n")