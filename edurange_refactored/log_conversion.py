#TODO Make func to input filename and to run from cmd line
import pandas as pd
import json
from pandas import DataFrame
from datetime import datetime
import time
#The following does not work due to the way the CSV file handles newlines within quoted text.
#log = pd.read_csv("test.csv", quoting=0, sep = '|', quotechar = '"')

#Built Replacement for read_csv
quoteChar = '%'
sepChar = '|'
newLineChar = '\n'
specialChar = '\\'
section = ""
lineData = []
logData = []
file = open("sample_fw_history.csv")
fileCont = True #Allows for exiting the read within its multiple loops
while fileCont:
	nextChar = file.read(1)
	if not nextChar:
		fileCont = False
		break
	if nextChar == quoteChar and section == "": #If the fist character after a new delinitation is quoted, do the following
		section = nextChar
		while fileCont:
			nextChar = file.read(1)
			if not nextChar:
				fileCont = False
				break
			elif nextChar == quoteChar:
				section+=nextChar
				break
			elif nextChar == newLineChar:
				nextChar = "\\n"
			elif nextChar == specialChar:
				section+=specialChar
			section+=nextChar
	elif nextChar == sepChar:
		lineData.append(section)
		section = ""
	elif nextChar == newLineChar:
		lineData.append(section)
		section = ""
		logData.append(lineData)
		lineData = []
	else:
		section+=nextChar
		
log = pd.DataFrame(logData) #Convert to pandas for easier manipulation
log = log.rename(columns=log.iloc[0])  #Rename the display columns to the provided titles and drop that first entry
log = log[log['#INPUT'] != '#INPUT']
log = log.dropna(subset=['time']) #Drop invalid rows
log = log.iloc[:,:-2]
inputSplit = log['node:input'].str.split(':', n=1, expand=True) #Just get what the user typed
host = inputSplit[0]
inputSplit = inputSplit[1].str.split(';|\||<|>', expand=True) #Separate out multiple commands typed in a single line
log.insert(loc = 7, value = inputSplit[0], column = 'Command')

#Create the data requested
utc = []
for tim in log['time']:
	utc.append(datetime.fromtimestamp(time.mktime(time.localtime(int(tim)))).strftime('%Y-%m-%dT%H:%M:%S%Z')) #Convert Unix time to a more standard format.
log.insert(loc = 0, column = 'timestamp_str', value = utc) #Move the required data
log.insert(loc = 1, column = 'cmd', value = log['Command'])
log.insert(loc = 2, column = 'username', value = log['uid'])
log.insert(loc = 3, column = 'hostname', value = host)
log.insert(loc = 4, column = 'wd', value = log['cwd'])
log.to_json('tes.json')#Oupt to the JSON file
