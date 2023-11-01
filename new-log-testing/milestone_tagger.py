'''
milestone tagger

'''
import sys
import yaml
import pprint
import csv
import re


def apply_regexes(regex_list, csv_line, milestone_bitvector):

    stdin = csv_line[4]

    #print(input)


    for r in regex_list:
        potential_match = re.match(r, stdin)
        
        if potential_match is not None:
            print(potential_match)


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

    with open("milestones.yml", "r") as yml:
        document = yaml.full_load(yml)
        
        #pp.pprint(document[0])
        
        regexes = document[0]["Milestones"]["Regexes"]
        
        #print(regexes.keys())

        #for item in regexes.items():
        #    print(item[1])

    csvFile = open("untagged.csv", "r")

    reader = csv.reader(csvFile, delimiter=',', quotechar='%', quoting=csv.QUOTE_MINIMAL)
    
    untagged = []
    milestone_bitvector = []
    for row in reader:
        apply_regexes(regexes, row, milestone_bitvector)

    #print(untagged)
    #print(regexes)


