from sys import stdin, stdout
from argparse import ArgumentParser
from csv import writer as csvwriter
from milestone import load_milestones, toy_yield_log, yield_log, \
                      milestone_tagger

def create_argv_parser():
  description = 'Process and tag a ttylog session file according to '\
                'a collection of milestone expressions'
  parser = ArgumentParser(description=description)
  
  parser.add_argument('milestonef', default='milestones.yml')
  
  input_argstrings = ['--inputf', '--input', '--in', '-i']
  parser.add_argument(*input_argstrings, default=stdin)
  
  output_argstrings = ['--outputf', '--output', '--out', '-o']
  parser.add_argument(*output_argstrings, default=stdout)
  
  parser.add_argument('--toy', '--test', '-t', action='store_true')
  
  return parser
  
def main_loop(tagger, destination):
  writer = csvwriter(destination, delimiter=',', quotechar='%')
  for line in tagger:
    matched, results, original_text = line
    writer.writerow(original_text + [rank for rank, _ in results])

if __name__ == '__main__':
  parser = create_argv_parser()
  arguments = parser.parse_args()
  
  milestones_deserialized = load_milestones(arguments.milestonef)
  
  if arguments.toy:
    log_iterable = toy_yield_log(arguments.inputf)
  else:
    log_iterable = yield_log(arguments.inputf)
  
  tagger = milestone_tagger(milestones_deserialized, log_iterable)
  
  output_f = arguments.outputf
  if output_f is not stdout:
    output_f = open(arguments.outputf, 'w', newline='')
  
  main_loop(tagger, output_f)
  
  if output_f is not stdout:
    output_f.close()