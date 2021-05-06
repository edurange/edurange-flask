import csv

from edurange_refactored.extensions import db
from edurange_refactored.user.models import Scenarios


def readCSV(id):
    db_ses = db.session
    sName = str(db_ses.query(Scenarios.name).filter(Scenarios.id == id).first()[0])
    sName = "".join(e for e in sName if e.isalnum())
    csvFile = open("./data/tmp/" + sName + "/" + sName + "-history.csv", "r")
    arr = []
    reader = csv.reader(csvFile, delimiter="|", quotechar="%", quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        if len(row) == 8:
            arr.append(row)
    return arr


def readCSV_by_name(name):
    csvFile = open("./data/tmp/" + name + "/" + name + "-history.csv", "r")
    arr = []
    reader = csv.reader(csvFile, delimiter="|", quotechar="%", quoting=csv.QUOTE_MINIMAL)
    for row in reader:
        if len(row) == 8:
            arr.append(row)

    return arr


def groupCSV(arr, keyIndex): # keyIndex - value in csv line to group by
    dict = {}
    for entry in arr:
        key = str(entry[keyIndex].replace('-', ''))
        if key in dict:
            dict[key].append(entry)
        else:
            dict[key] = [entry]
    return dict
