'''
milestone tagger

'''
import sys
import yaml
import pprint
import csv
import re
import numpy as np
import os


ERRORS = [
        "Invalid mode",
        "Invalid option",
        "No such file or directory",
        "Permission denied",
        "Command Interrupted ^C",
        "Segmentation Fault (Core Dumped)",
        "Syntax Error",
        "Out of memory",
        "Command not found",
        "Argument list too long",
        ]

def detect_error(output_line, ERRORS):
    error_tag = "s"
    for e in ERRORS:
        if e in output_line:
            error_tag = "f"
    return error_tag

def detect_overflow(output_line):
    #TODO
    pass



def levenshtein(s, t):            #checks similarities between two words
    rows = len(s) + 1
    cols = len(t) + 1
    deletes = 1
    inserts = 1
    substitutes = 1
    dist = [[0 for x in range(cols)] for x in range(rows)]

    for row in range(1,rows):
        dist[row][0] = row * deletes
    for col in range(1, cols):
        dist[0][col] = col * inserts
    for col in range(1,cols):
        for row in range(1,rows):
            if s[row-1] == t[col-1]:
                cost = 0
            else:
                cost = substitutes
            dist[row][col] = min(dist[row-1][col] + deletes, dist[row][col-1] + inserts, dist[row-1][col-1] + cost)
    return dist[row][col]

def apply_regexes(regex_list, csv_line, milestone_bitvector):

    stdin = ""
    if len(csv_line) >= 4:
        stdin = csv_line[4]
        command, args = parse_stdin(stdin)       
        
    for milestone, r in enumerate(regex_list.values()):
        potential_match = re.match(r, stdin)
        
        distance = levenshtein(r, stdin)
        print(distance)

        if potential_match is not None:
            milestone_bitvector[milestone] = 1
            #print(potential_match)

    print(milestone_bitvector)

def parse_stdin(stdin_line):
    command = ""
    args = ""
    return command, args


def decompose_line(line):
    """
    Split the csv file into a list of lists where each item is one log entry

    column indexes:
        0: edulog (Experiment name: Starting Timestamp)
        1: Hostname
        2: Start Timestamp
        3: Working Dir
        4: Input Command (Plus args, Plus error)
        5: Output (Contains newlines)
        6: Prompt (user@hostname)
    """
    #print(line)
    try:
        components = {
                "hostname": line[1],
                "timestamp": line[2],
                "directory": line[3],
                "stdin" : line[4],
                "output": line[5],
                "prompt": line[6]
                }
        return components

    except IndexError:
        print("Found incomplete log line")
        #exit(0)

def handle_input_milestone(mstone, line):
    # TODO 
    #print("Found INPUT")
    pass

def handle_output_milestone(mstone, line):
    # TODO 

    desired_output = str(mstone["Output"])
    found_output = line["output"]

    print(f"Checking Line: {line}")
    print(f"Want output: {desired_output}")
    print(f"Found output: {found_output}\n")

    if desired_output in found_output:
        print("MATCHED OUTPUT")
        exit(0)

    pass

def handle_compound_milestone(mstone, line):
    # TODO 
    #print("Found COMPOUND")
    pass


def process_logs(log_dir, milestones):
    for file in os.listdir(log_dir):
        filename = os.fsdecode(file)

        if filename.endswith(".csv"):
            process_student_log(log_dir, filename, milestones)

def process_student_log(log_dir, filename, milestones):
        with open(os.path.join(log_dir, filename), 'r') as csv_file:
            reader = list(csv.reader(csv_file, delimiter=',', quotechar='%', quoting=csv.QUOTE_MINIMAL))

            #print(reader)
            #print(filename)
            #print(milestones)


            for l in reader:
                line = decompose_line(l)
                #print(line)
                if line is None:
                    continue

                for i, mstone in enumerate(milestones):
                    print(mstone)
                    mstone_type = mstone["Type"]
                    # Breaks if not on python 3.10 TODO update docker images
                    match mstone_type:
                        case 'Input':
                            handle_input_milestone(mstone, line)

                        case "Output":
                            handle_output_milestone(mstone, line)

                        case "Compound":
                            handle_compound_milestone(mstone, line)

                        case _:
                            raise Exception("Unknown Milestone Type Encountered")

                    #print(type(m))




if __name__ == "__main__":
    '''
  Milestone file is a .yml file

  Old finished tagged product:
      INPUT|066ec2--39|M10 |1579211665|066ec2|cp file2.txt copied_file2.txt|OUTPUT|/home/066ec2/manipulate

  Raw data:
      edulog:1696113508:0,NAT,1696113525,/home/devuser1,ls,%
    editme  final-mission  followMe  i  stuff  textfiles  toLearn
    devuser1@NAT%,devuser1@NAT:~

  '''
    """
  for k, cmd in enumerate(stdin):
            if k == 0 or stdin[0] == 'sessions':
                for ec in expected_cmds:
                    if re.fullmatch(ec, cmd):
                        found_cmd = True
            else:
                for eo in expected_opts:
                    if eo == '':
                        continue
                    if re.match(eo, cmd):
                        #print("Options Matched: {} - {}".format(eo, cmd))
                        found_opt = True
    """

    pp = pprint.PrettyPrinter(indent=4)
    if len(sys.argv) != 4:
        print('usage:\n milestone_tagger.py <log_dir> <milestone_file> <out_dir>')
        exit(1)

    # Read Arguments
    log_dir = sys.argv[1]
    milestone_file = sys.argv[2]
    out_dir = sys.argv[3]

    with open(milestone_file, "r") as yml:
        document = yaml.full_load(yml)
        
        #pp.pprint(document[0])
        
        # Create the list of milestones, each milestone is a dictionary
        milestones = document[0]["Milestones"]["Prototype"]
        
        #print(regexes.keys())

        #for item in regexes.items():
        #    print(item[1])

    process_logs(log_dir, milestones)

    

    #pp.pprint(reader)
    

   
    
    #num_milestones = len(regexes)
    #milestone_bitvector = np.zeros(num_milestones)

   # for row in reader:
   #     apply_regexes(regexes, row, milestone_bitvector)

    #print(untagged)
    #print(regexes)
