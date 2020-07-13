import csv
import sys
csvFile = open(sys.argv[1], 'r')
tsvFile = open(sys.argv[2], 'w')

arr = []
reader = csv.reader(csvFile, delimiter=',', quotechar='%', quoting=csv.QUOTE_MINIMAL)

for row in reader:
    lineStr = ''
    for i,item in enumerate(row):
        if i == 5:
            item = item.replace("\r", "").replace("\n", "")
            item = item.replace('\"', '').replace(",", "")
            item = item.replace('\t', '')
        if i == 0:
            lineStr += item.strip('\n\r')
        else:
            lineStr += '\t' + item.strip('\n\r')
        if i == 6:
            lineStr += '\n'
    arr.append(lineStr)
for a in arr:
    tsvFile.write(a)
