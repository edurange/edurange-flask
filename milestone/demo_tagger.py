from sys import stdin, stdout
from argparse import ArgumentParser
from csv import writer as csvwriter

from milestone import load_milestones, toy_yield_log, yield_log, \
                      milestone_tagger 

"""
Demonstrates how to set up and run the tagger. In this case, a little 
extra functionality has been added so that toy_yield_log can be called 
to interpret log lines, reducing the number of CSV columns that need to 
be provided for test/sample input.
"""
"""
Please note that argparse is a standard Python library and is used only 
to parse sys.argv for invocation options. It is not involved in the 
interpretation of milestones.
"""
def main_loop(tagger, destination):
  writer = csvwriter(destination, delimiter=',', quotechar='%')
  for line in tagger:
    """
    For lack of a better output policy right now, we simply append the 
    results of milestone evaluation to the end of the original CSV 
    columns.
    """
    """
    The tagger returns three items at each iteration. matched is a 
    dict[<users>] -> dict[<milestone labels>] -> [<timestamps>]. 
    results is a nested list/dict/tuple object representing the 
    intermediate results of the evaluation of each milestone, where 
    each tuple contains a confidence value in the first position and 
    the evaluated milestone subexpression in the second position. 
    original_text is the original log line before being split by 
    csv.reader.
    """
    matched, results, original_text = line
    output_text = original_text + [rank for rank, _ in results]
    writer.writerow(output_text)

if __name__ == '__main__':
  def create_argv_parser():
    """
    Creates an argparse.ArgumentParser to grab parameters out of argv. 
    The parser object will then create an arguments object that has the 
    information we want from the command line.
    """
    description = 'Process and tag a ttylog session file according '\
                  'to a collection of milestone expressions'
    parser = ArgumentParser(description=description)
    
    parser.add_argument('milestonef', default='milestones.yml')
    
    input_argstrings = ['--inputf', '--input', '--in', '-i']
    parser.add_argument(*input_argstrings, default=stdin)
    
    output_argstrings = ['--outputf', '--output', '--out', '-o']
    parser.add_argument(*output_argstrings, default=stdout)
    
    parser.add_argument('--toy', '--test', '-t', action='store_true')
    
    return parser
  
  parser = create_argv_parser() # Defines how to parse arguments.
  arguments = parser.parse_args() # Gets the parsed arguments.
  
  # Load a YAML file of milestones, with a little error checking.
  milestones_deserialized = load_milestones(arguments.milestonef)
  print(milestones_deserialized)
  
  # Load a log source, which can be a file handler or a path string.
  if arguments.toy:
    log_iterable = toy_yield_log(arguments.inputf)
  else:
    log_iterable = yield_log(arguments.inputf)
  
  """
  The tagger is a generator function - a function that is also an 
  iterator. That means we can consume the results it returns with a for 
  loop like a list. The generator maintains its own internal state 
  while we consume elements from it. In the case of the tagger, it 
  maintains a record of where it is in the log file and what milestones 
  have already been matched.
  """
  tagger = milestone_tagger(milestones_deserialized, log_iterable)
  
  output_f = arguments.outputf
  if output_f is not stdout:
    output_f = open(arguments.outputf, 'w', newline='')
  
  main_loop(tagger, output_f)
  
  if output_f is not stdout:
    output_f.close()