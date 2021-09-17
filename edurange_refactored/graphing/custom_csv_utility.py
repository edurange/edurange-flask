""" Module for handling csv imports and possibly yaml content on milestone information"""
import csv
from datetime import datetime

from flask.globals import current_app

def file_load(file_name, scenario):
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
    csv_file = open("./edurange_refactored/graphing/" + file_name, 'r')
    reader = csv.reader(csv_file, delimiter="|", quotechar="%", quoting=csv.QUOTE_MINIMAL)

    log = []

    #this is where the milestone and report nodes are built
    #currently from a file but to be created from yaml info
    milestones = append_milestones(scenario + '_' + 'ms_nodes.csv')
    count = len(milestones)
    
    for item in milestones:
        log.append(item)

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

    count = len(log)
    reports = append_reports(scenario + '_' + 'report_nodes.csv', count)
        
    for item in reports:
        log.append(item)

    csv_file.close()
    # for item in log:
    #     print(item)
    return log

def db_log_load(log_obj, scenario):
    """
    Loads db query into data structure usable for graphviz.

    Parameters
    -------
    log_obj : however it comes out of database query
    scenario : plain text <scenario_name>

    Returns
    -------
    log object todo...
    """
    
    log = []
    
    #this is where the milestone and report nodes are built
    #currently from a file but to be created from yaml info
    milestones = append_milestones(scenario + '_' + 'ms_nodes.csv')
    count = len(milestones)
    #call function to format database query
    log_entries = format_query(log_obj, count)
    
    for item in milestones:
        log.append(item)

    for item in log_entries:
        log.append(item)

    count = len(log)
    # current_app.logger.info(f'###COUNT: {count}')
    reports = append_reports(scenario + '_' + 'report_nodes.csv', count)
        
    for item in reports:
        log.append(item)

    # for item in log:
    #     print(item)
    return log

def format_query(log_obj, cnt):
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
    count = cnt
    log = []

    #for each entry in database query object
    for entry in log_obj:
        #may need to revisit this to remove 'U' tagged items
        #do not insert nodes with 'U' tags
        if 'U' not in entry[1]:
            count += 1
            user = entry[0].split('-')[0]
            tmp = str(entry[1]).split()
            milestone = sorted(tmp, reverse=True)[0]
            timestamp = entry[2].ctime()
            command = entry[3] #.split(':')[-1]
            event = [count, user, milestone, timestamp, command]
            log.append(event)

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
    csv_file = open('./edurange_refactored/graphing/cli_tool/csv_templates/' + file_name, 'r')
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

def append_reports(file_name, cnt):
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
    csv_file = open('./edurange_refactored/graphing/cli_tool/csv_templates/' + file_name, 'r')
    reader = csv.reader(csv_file, delimiter="|", quotechar="%", quoting=csv.QUOTE_MINIMAL)
    #f = open(file_name, 'r')
    count = cnt
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

