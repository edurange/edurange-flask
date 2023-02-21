#!/usr/bin/env python3
import subprocess
import sys

s = sys.stdin.readlines() #reads text from stdin to s

s = s[0] #resets s to be the 0th entry of the list from stdin

l = s.split('+') #splits the raw text around '+' introduced in db query in extract_logs.sh, giving individual lines

fields=["id","user_id","scenario_id","question","student_response","points","response_time","attempt"] #creates field lables

sOut = ",".join(fields)+"\n" #initialized string to write otu with field lables at top of csv

for record in l: #iterates through each list entry (line of log) from l
    thing = record.split('|') #removes '|' characters from lines of log
    sOut += ",".join(thing) + "\n" #concatonates line to the text for the .csv


sOut = sOut.strip() #removes any transient spaces

#print(sOut) #prints to term(for debugging)

with open("../logs/MLoutfile.csv", "w") as fh: #writes the csv and exits python
    fh.writelines(sOut)
    exit()