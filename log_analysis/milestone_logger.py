import sys
import re
import os
import csv
from datetime import datetime
from tabulate import tabulate


# This function populates the commands dictionary
# Each user is stored as a key, values are a list of lists with timestamp, command
def filter_to_minimal():
    with open(log_file, 'r') as csv_file:
        # Read reversed to have correct chronological order
        testreader = reversed(list(csv.reader(csv_file, delimiter=',')))
        for row in testreader:
            if len(row) > 0:
                # Skip if header row
                if row[0] == 'performed_at':
                    continue
                else:
                    # Strip timestamp to only HH:MM:SS
                    timestamp = row[0].split()[1]
                user_name = row[4]
                # Read command, replace commas to prevent csv problems
                com = row[6].replace(",", ".")
                com.replace(r';', '.')
                # Check if user is in the dictionary, if not initialize and append first 'timestamp, command'
                if user_name not in commands.keys():
                    commands[user_name] = []
                    achievement_list[user_name] = []
                    commands[user_name].append('{} {}'.format(timestamp, com) if len(user_name) > 0 else row[4])
                # If user is already stored as a key, just append new 'timestamp, command' list
                else:
                    commands[user_name].append('{} {}'.format(timestamp, com) if len(user_name) > 0 else [row[4]])
    # Write to temp file
    with open(out_file, 'w') as tmp:
        tmp.write('user, timestamp, command, milestone_check, elapsed_lastM\n')
        for key in commands.keys():
            if key == 'player_login':
                continue
            for item in commands[key]:
                item = item.split()
                # Write user and timestamp as comma separated columns, then join the rest of the command in last col
                tmp.write(key + ', ' + item[0] + ', ' + " ".join(item[1:]) + '\n')


# This function populates the milestones and patterns
def read_milestones():
    with open(milestone_file, 'r') as m_file:
        m_reader = list(csv.reader(m_file, delimiter=','))
        for row in m_reader:
            patterns.append(row[1:])
            milestones[row[0]] = row[1:]

        # Here create a bit vector for all milestones (M0 is a placeholder)
        for key in achievement_list:
            for i in range(len(milestones) + 1):
                if i == 0:
                    achievement_list[key].append(1)
                else:
                    achievement_list[key].append(0)


def annotate_milestones():
    # Read the filtered temp output file
    with open(out_file, 'r') as temp:
        # Open a file to write tagged lines
        with open(out_file + '-tagged', 'w') as tags_out:
            for line in temp:
                # Clean up lines and split to list
                line = line.strip('\n')
                line = line.split(', ')
                # Set default tag to unrelated
                tag = 'U'
                # Mark the Header line
                if line[0] == 'user':
                    tag = 'H'
                # 'patterns' contains a list of regex for each milestone
                for mstone in patterns:
                    # Read individual patterns for each milestone:
                    for p in mstone:
                        # Partial matches mean attempts, will be overwritten if there's a full match
                        if re.match(p, line[2]) is not None:
                            # Determine associated milestone:
                            for m, pats, in milestones.items():
                                if p in pats:
                                    if not tag.startswith('M'):
                                        tag = 'A' + m[1]
                        # Full matches mean milestone complete
                        if re.fullmatch(p, line[2]) is not None:
                            # Determine the milestone associated with the matched pattern:
                            for m, pats in milestones.items():
                                if p in pats:
                                    # If first completion, mark with M# and mark complete
                                    if achievement_list[line[0]][int(m[1:])] == 0:
                                        tag = m
                                        achievement_list[line[0]][int(m[1:])] = 1
                                        continue
                                    # If previously completed, mark as verification
                                    else:
                                        tag = 'V - ' + m
                        # If student is using manual, mark it as related (Except if its a milestone)
                        if re.match('^man', line[2]) is not None:
                            if tag.startswith('M'):
                                pass
                            else:
                                tag = 'R'
                line.append(tag)
                for i in range(len(line)):
                    if i != len(line) - 1:
                        tags_out.write(line[i] + ', ')
                    else:
                        tags_out.write(line[i])
                tags_out.write('\n')


def calculate_timing():
    with open(out_file + '-tagged', 'r') as tag_file:
        with open(out_file + '-timed-and-tagged.csv', 'w') as time_file:
            # Initialize necessary variables
            count = 0
            last_time = ''
            elapsed = '00:00:00'
            header = ''
            for line in tag_file:
                line = line.strip('\n')
                line = line.split(', ')
                # Write the header separately before considering time operations
                if count == 0:
                    header = line
                    for col in header:
                        time_file.write(col + ', ')
                    time_file.write('\n')
                    count += 1
                    continue
                # First row determines start time
                if count == 1:
                    last_time = datetime.strptime(line[1], "%H:%M:%S")
                else:
                    tag = line[3]
                    time = datetime.strptime(line[1], "%H:%M:%S")
                    elapsed = time - last_time
                    elapsed = str(elapsed)
                    # If tag is a milestone completion, update the time baseline
                    if tag[0] == 'M':
                        last_time = time
                count += 1
                line.append(elapsed)
                for i in range(len(line)):
                    if i != len(line) - 1:
                        time_file.write(line[i] + ', ')
                    else:
                        time_file.write(line[i])
                time_file.write('\n')


if __name__ == "__main__":
    # Proper usage check
    if len(sys.argv) != 4:
        print('usage:\n milestone_logger.py <log_file> <milestone_file> <out_file>')
        exit(1)

    # Read Arguments
    log_file = sys.argv[1]
    milestone_file = sys.argv[2]
    out_file = sys.argv[3]

    # Initialize storage
    commands = {}
    milestones = {}
    patterns = []
    achievement_list = {}

    # Read only 'user, timestamp, command' from csv
    filter_to_minimal()

    read_milestones()
    annotate_milestones()

    calculate_timing()

    for key in achievement_list:
        print(key + ' - Milestones completed: - ' + ' '.join(str(i) for i in achievement_list[key] if key != 0))

    # Clean up temp files
    os.remove(out_file)
    os.remove(out_file + '-tagged')
