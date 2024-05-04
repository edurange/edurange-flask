from csv import reader as csvreader
from yaml import load as yamlloader
try: # Use the C-native implementation if it's available
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader
from itertools import count

USER = 'user'
TIMESTAMP = 'timestamp'
NODE = 'node'
INPUT = 'input'
OUTPUT = 'output'

# Log handling helpers
def object_identity(obj):
  return obj

def remove_null_bytes(string):
  return string.replace('\0', '')

def yield_csv(
    filename, delimiter='|', quotechar='%', 
    filter_f = object_identity):
  """
  Generates a list of strings according to a csv file. Provide filter_f  
  a function str -> str to pre-process the input text (eg for error 
  correction) before csv.reader attempts to parse it.
  """
  with open(filename, newline='') as file:
    filtered_text = (filter_f(line) for line in file)
    for line in csvreader(filtered_text, delimiter=delimiter, 
        quotechar=quotechar):
      yield line

def yield_log(filename):
  """
  A generator function that yields the log line-by-line, with relevant 
  columns (input, output, etc) pre-processed into a dict of 
  properties. This can be re-implemented and its references swapped in 
  the main portion of the script to support different log format 
  versions.
  """
  # Sample logs have null bytes which csv.reader cannot handle, so I'm 
  # providing a filter function to use before csv.reader gets the input
  for line in yield_csv(filename, filter_f=remove_null_bytes):
    try: # This version is very permissive of bad log lines
      user_text = line[1]
    except IndexError:
      user_text = ''
    
    try:
      timestamp_text = line[3]
    except IndexError:
      timestamp_text = ''
    
    try:
      prompt = line[6].split(':')
    except IndexError:
      prompt = ['', '']
    
    node_text = prompt[0]
    
    try: # split() could return a list of length 1
      input_text = prompt[1]
    except IndexError:
      input_text = ''
      
    try:
      output_text = line[7]
    except IndexError:
      output_text = ''
      
    yield {
            USER: user_text,
            TIMESTAMP: timestamp_text,
            NODE: node_text,
            INPUT: input_text, 
            OUTPUT: output_text
    }
  """
  Consider changing dict representation to a @dataclass for 
  compactness. String dict keys come with redundant reference clutter; 
  trying to save space here by using marker objects as keys instead of 
  plain strings. See also typing.Literal for a possible improvement.
  
  May need to implement a separate log loader module that does the 
  error handling and cleaning elsewhere for clarity.
  """

def toy_yield_log(filename):
  """
  As above, but with a simplified log format for early testing. The 
  bare minimum of what a log handling generator should do.
  """
  for line in yield_csv(filename, delimiter=','):
    yield {
            USER: line[0],
            TIMESTAMP: line[1],
            NODE: line[2],
            INPUT: line[3], 
            OUTPUT: line[4]
    }
    
# Milestone file handling helpers
def load_yaml(filename):
  """
  Interprets a YAML file as a list of nested dicts, lists and literals
  """
  with open(filename) as file:
    contents = yamlloader(file, Loader=Loader)
  
  return contents
  
def label_anonymous_milestones(milestones):
  """
  Adds a 'label' key-value pair to each dict in a list of milestone 
  dicts, if 'label' was not already present
  """
  num = count()
  for milestone in milestones:
    if 'label' not in milestone.keys():
      milestone['label'] = f'Anonymous Milestone {next(num)}'
  
  return milestones

def load_milestones(filename):
  return label_anonymous_milestones(load_yaml(filename))
  
"""
Questions:
  - Do we want to coerce values on loading - ie should timestamps be 
    converted from strings to ints? How do we want to handle 
    irregularities?
  - Double dicts and other such nested iterators are discouraged - 
    should we consider a class interface for the return structure? Or 
    switch to a numpy matrix/pandas dataframe?
To Do:
  - Consolidate IndexError try blocks in yield_log.
  - Consider pandas for normalizing log and output representations.
"""