""" Module for handling csv imports and possibly yaml content on milestone information"""
import csv

def file_load(file_name):
    """
    Loads csv into data structure usable for graphviz.

    Parameters
    -------
    file_name : <filename.csv>

    Returns
    -------
    log object todo...
    """
    #ignore linter error, csv_file is closed at end...
    csv_file = open(file_name, 'r')
    reader = csv.reader(csv_file, delimiter="|", quotechar="%", quoting=csv.QUOTE_MINIMAL)

    log = []

    #this is where the milestone and report nodes are built
    #currently from a file but to be created from yaml info
    milestones = append_milestones('milestone_nodes.csv')
    reports = append_reports('report_nodes.csv')

    for item in milestones:
        log.append(item)

    count = 16

    #for each entry in csv log
    for line in reader:
        if len(line) != 8:
            continue
        count += 1
        #do not insert nodes with 'U' tags
        #if parts[2] != 'U':
        user = line[4]
        milestone = line[2]
        timestamp = line[3]
        command = line[6]#.split(':')[-1]
        event = [count, user, milestone, timestamp, command]
        log.append(event)

    for item in reports:
        log.append(item)

    csv_file.close()
    for item in log:
        print(item)
    return log

def append_milestones(file_name):
    """
    Loads csv into data structure usable for graphviz.

    Note!!! This will be replaced by a yaml reader

    Parameters
    -------
    file_name : <filename.csv>

    Returns
    -------
    log object todo...
    """
    csv_file = open(file_name, 'r')
    reader = csv.reader(csv_file, delimiter="|", quotechar="%", quoting=csv.QUOTE_MINIMAL)
    #f = open(file_name, 'r')
    count = 0
    log = []
    #for each entry in csv log
    for line in reader:
        if len(line) != 8:
            continue
        count += 1
        #do not insert nodes with 'U' tags
        #if parts[2] != 'U':
        user = line[4]
        milestone = line[2]
        timestamp = line[3]
        command = line[6]#.split(':')[-1]
        event = [count, user, milestone, timestamp, command]
        log.append(event)
    csv_file.close()
    #for e in log:
    #    print(e):
    return log

def append_reports(file_name):
    """
    Loads csv into data structure usable for graphviz.

    Note!!! This will be replaced by a yaml reader.

    Parameters
    -------
    file_name : <filename.csv>

    Returns
    -------
    log object todo...
    """
    csv_file = open(file_name, 'r')
    reader = csv.reader(csv_file, delimiter="|", quotechar="%", quoting=csv.QUOTE_MINIMAL)
    #f = open(file_name, 'r')
    count = 89
    log = []
    #for each entry in csv log
    for line in reader:
        if len(line) != 8:
            continue
        count += 1
        #do not insert nodes with 'U' tags
        #if parts[2] != 'U':
        user = line[4]
        milestone = line[2]
        timestamp = line[3]
        command = line[6]#.split(':')[-1]
        event = [count, user, milestone, timestamp, command]
        log.append(event)
    csv_file.close()
    return log

