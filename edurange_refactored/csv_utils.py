import csv

from edurange_refactored.extensions import db
from edurange_refactored.user.models import Scenarios


def readCSV(value, attribute):
    if attribute == 'id':
        sName = db.session.query(Scenarios.name).filter(Scenarios.id == value).first()[0]
        sName = "".join(e for e in sName if e.isalnum())
    else:
        sName = value

    fd = open(f"./data/tmp/{sName}/{sName}-history.csv")
    reader = csv.reader(fd, delimiter="|", quotechar="%", quoting=csv.QUOTE_MINIMAL)

    return [row for row in reader if len(row) == 8]


def groupCSV(arr, keyIndex): # keyIndex - value in csv line to group by
    dict = {}
    for entry in arr:
        key = str(entry[keyIndex].replace('-', ''))
        if key in dict:
            dict[key].append(entry)
        else:
            dict[key] = [entry]

    return dict
