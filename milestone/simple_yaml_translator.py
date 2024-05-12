from sys import stdin, stdout
from argparse import ArgumentParser
from csv import reader as csvreader
from yaml import dump as yamldump

NODE = 'node'
INPUT = 'input'
OUTPUT = 'output'

"""
Generates a simple YAML representation based on the three-column CSV 
format previously used. Unfortunately yaml.dump does not use the 
generic iterator method when reading dicts, and so properties come out 
in alphabetical order despite attempts to manipulate insertion order or 
use of dict subclasses.
"""

def create_argv_parser():
  description = 'Convert a three-column CSV milestone file to a YAML '\
                'milestone file'
  parser = ArgumentParser(description=description)
  
  input_argstrings = ['--inputf', '--input', '--in', '-i']
  parser.add_argument(*input_argstrings, default=stdin)
  
  output_argstrings = ['--outputf', '--output', '--out', '-o']
  parser.add_argument(*output_argstrings, default=stdout)
  
  return parser

if __name__ == '__main__':
  parser = create_argv_parser()
  arguments = parser.parse_args()
  
  input_f = arguments.inputf[0]
  if input_f is not stdin:
    input_f = open(input_f, newline='')
  
  output_f = arguments.outputf[0]
  if output_f is not stdout:
    output_f = open(output_f, 'w', newline='')
  
  csv_columns = [NODE, INPUT, OUTPUT]
  for i, csv_line in enumerate(csvreader(input_f)):
    milestone_dict = dict(zip(csv_columns, csv_line))
    for row in list(milestone_dict.keys()):
      if milestone_dict[row] == '*' or milestone_dict[row] == '':
        del milestone_dict[row]
    milestone_dict['label'] = f'M{i}'
    yamldump([milestone_dict], output_f, default_flow_style=False)
    output_f.write('\n')
  
  if arguments.outputf is not stdout:
    output_f.close()