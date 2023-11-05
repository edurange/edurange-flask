'''
milestone tagger

'''
import sys
import yaml
import pprint
import csv
import re
import numpy as np


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


def identify_milestone_type(milestone):
    # TODO 
    
    #found_type = milestone[0]["Type"]

    #return found_type

    pass

def handle_input_milestone(found_type):
    # TODO 

    pass

def handle_output_milestone(found_type):
    # TODO 

    pass

def handle_compound_milestone(found_type):
    # TODO 

    pass



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
    
    # Proper usage check
 #   if len(sys.argv) != 3:
 #      print('usage:\n master_log_tagger.py <milestone_file> <log_file> <out_file>')
 #     exit(1)

    with open("proto_milestones.yml", "r") as yml:
        document = yaml.full_load(yml)
        
        #pp.pprint(document[0])
        
        milestones = document[0]["Milestones"]["Prototype"]
        
        #print(regexes.keys())

        #for item in regexes.items():
        #    print(item[1])

    csvFile = open("untagged.csv", "r")

    reader = csv.reader(csvFile, delimiter=',', quotechar='%', quoting=csv.QUOTE_MINIMAL)
    
    

    for index, m in enumerate(milestones):
        mstone_type = m["Type"]
    
        #mnumber = index + 1

        #mtag = "M" + mnumber

        pp.pprint(m["Type"])
        
        # Breaks if not on python 3.10 TODO update docker images
        match mstone_type:
            case 'Input':
                handle_input_milestone(m)

            case "Output":
                handle_output_milestone(m)

            case "Compound":
                handle_compound_milestone(m)

            case _:
                raise Exception("Unknown Milestone Type Encountered")

        #print(type(m))

    untagged = []
    
    #num_milestones = len(regexes)
    #milestone_bitvector = np.zeros(num_milestones)

   # for row in reader:
   #     apply_regexes(regexes, row, milestone_bitvector)

    #print(untagged)
    #print(regexes)


