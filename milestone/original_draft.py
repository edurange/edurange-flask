from collections import defaultdict
from regex import search
from yaml import load
try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader 
from csv import reader as csvreader

# some helpers and abstractions
def extract_input(log_line):
  """decouples the log format from the parsing behavior"""
  return log_line[0]
  
def extract_output(log_line):
  """decouples the log format from the parsing behavior"""
  return log_line[1]

def to_arg_list(value_parameters):
  """
  makes things into lists so we can use yaml attributes like n-tree 
  nodes
  """
  args = []
  if isinstance(value_parameters, list):
    args = value_parameters
  elif isinstance(value_parameters, dict):
    # derivatives can parse options/keywords here
    # 'args' isn't guaranteed to be a list - is this a problem?
    args = value_parameters['args']
  else:
    args = [value_parameters]
  return args
  
def to_arg_dict(value_parameters):
  """
  packs lists and literals into a dict so that parse methods can have 
  standardized patterns for parameter handling
  """
  args = value_parameters
  if not isinstance(value_parameters, dict):
    args['args'] = to_arg_list(value_parameters)
  return args
  # if isinstance(value_paramters, dict):
  #   return value_parameters
  # else:
  #   return {'args': to_arg_list(value_parameters)}

def search_node(value_parameters, search_content):
  """helper function to dispatch regex.search over log text"""
  search_strings = to_arg_list(value_parameters)
  matched = False
  for string_pattern in search_strings:
    if search(string_pattern, search_content) is not None:
      matched = True
      break
  return matched
  
def label(milestone):
  return milestone['label']
# end helpers

def check_milestones(milestones_deserialized, log_stream):
  """"""
  found = defaultdict(list)
  parse_dispatcher = {}
  
  # these methods are responsible for parsing nodes of the milestone 
  # expression trees - helpers first
  def dispatch(key, value_parameters, log_line):
    try:
      parse_method = parse_dispatcher[key]
    except KeyError:
      print(f'dispatch: {key} not found - ignoring...')
      return False
    return parse_method(value_parameters, log_line)
    
  def fan_subnodes(expression_node, log_line):
    """fan and dispatch subexpression nodes"""
    results = []
    for key, value_parameters in expression_node.items():
      # omit or save/process special properties such as label
      if key in ['label', 'objective', 'comment']:
        continue
      else:
        sub_result = dispatch(key, value_parameters, log_line)
        results.append(sub_result)
    return results
  
  # dispatch table methods
  def parse_input(value_parameters, log_line):
    """search the input portion of log_line"""
    log_input = extract_input(log_line)
    return search_node(value_parameters, log_input)
    
  def parse_output(value_parameters, log_line):
    """search the output portion of log_line"""
    log_output = extract_output(log_line)
    return search_node(value_parameters, log_output)
    
  def parse_found(value_parameters, log_line):
    """checks the found record"""
    """
    note that results may be inconsistent for milestones matched on 
    the same line pass due to unpredictable dictionary ordering in 
    earlier Python implementations
    """
    search_labels = to_arg_list(value_parameters)
    results = [label for label in search_labels if label in 
                found.keys()]
    search_labels.sort()
    results.sort()
    return search_labels == results
  
  def parse_and(value_parameters, log_line):
    """performs n-ary and on the subnodes of value_parameters"""
    results = fan_subnodes(value_parameters, log_line)
    matched = True
    for result in results:
      if result is False:
        matched = False
    return matched
    
  def parse_or(value_parameters, log_line):
    """performs n-ary or on the subnodes of value_parameters"""
    results = fan_subnodes(value_parameters, log_line)
    matched = False
    for result in results:
      if result is True:
        matched = True
    return matched
    
  def parse_not(value_parameters, log_line):
    """boolean negation of the n-ary and of value_parameters"""
    matched = parse_and(value_parameters, log_line)
    return not matched
  # end parse methods
  
  parse_dispatcher |= {
      'input': parse_input,
      'output': parse_output,
      'found': parse_found,
      'and': parse_and,
      'or': parse_or,
      'not': parse_not
      }
  
  def match_milestone(milestone, log_line):
    """checks one milestone against one line"""
    results = fan_subnodes(milestone, log_line)
        
    if not results:
      # perhaps use an exception or log a descriptive error here
      return False
      
    matched = True
    for result in results:
      if result is False:
        matched = False
    return matched
  
  for line_index, log_line in log_stream:
    for milestone in milestones_deserialized:
      if match_milestone(milestone, log_line):
        found[label(milestone)].append(line_index)
    yield found



if __name__ == '__main__':
  # these helpers probably belong outside the milestone module in 
  # production so I hid them from the importable scope
  def load_yaml(filename):
    """creates a structure of lists/dicts according to a yaml file"""
    try:
      file = open(filename)
    except IOError:
      print(f'load_yaml: {filename} not found')
      quit()
    
    yaml_collection = load(file, Loader=Loader)
    file.close()
    
    return yaml_collection
    
  def stream_csv(filename):
    """generates a list of strings according to a csv file"""
    with open(filename, newline='') as stream:
      for line in csvreader(stream, delimiter=','):
        yield line
  # end helpers
    
  milestones_deserialized = load_yaml('milestones.yml')
  print(milestones_deserialized)
  
  log_stream = enumerate(stream_csv('log.csv'))
  print(log_stream)
  
  for found in check_milestones(milestones_deserialized, log_stream):
    print(found)
  
# Thoughts:
#
# Regarding milestones that depend on earlier milestones, what happens 
# when savvy students compose commands into one-liners? Do we want to 
# bother supporting such cases?
#
# Not sure what our use cases for are for hiding intermediate 
# milestones - I'd like to talk through that soon to make sure this 
# design doesn't get painted into a corner regarding how milestones 
# are referenced/indexed.
#
# Could add an expression keyword to limit parsing to just the 
# contents of that property, but the existing implementation has a 
# nice compactness so I kept it simple for now.
# 
# Could make labels optional; milestones without labels would then not 
# get logged in the found dict, and the label method would return none 
# when label is not found in the milestone keys.
# 
# The problem of undefined output for multiple milestones matched on 
# the same line in parse_found could potentially be addressed with 
# threads/coroutines and a priority queue.
# 
# When do we want this to run? Currently we post-process, but some 
# features have been proposed for displaying live milestone progress to 
# instructors. To support this behavior it might be good to design 
# milestone matching to run on a pipe or other live data source. 
# 
# How do we represent near matches - aka yellow nodes per Svabensky? 
# This likely calls for parse methods to return more than a simple 
# boolean value. The identification of yellow nodes is related to the 
# original attempt to categorize the input, so it seems reasonable that 
# yellow node coloring can be accomplished efficiently if incorporated 
# into the same algorithm that identifies green nodes - aka fully 
# matching milestones. Red node coloring is then trivially all nodes 
# that are neither green nor yellow. I'm very interested in inspecting 
# red nodes to see if they can yield predictive metrics about how 
# students' trajectories approach answers that partially or fully 
# match.

"""
milestoneparser
---
A proposal for specifying milestones in an extensible YAML format and 
searching CSV log files using the dict/list structures yielded by 
yaml.load.

Main entry point: check_milestones
- Iterates through the log and notes the labels and line indicies of 
  matched milestones. Takes a dictionary of milestone data (as per 
  yaml.load) and a list of strings representing the log contents line-
  by-line. Returns a dictionary of label strings mapped to lists of 
  matching lines.
- This method is a bit of a kludge. I used nested method definitions 
  and a nonlocal to avoid excessive parameter passing. I think I should 
  be able to move the dispatch table into its own class or coroutine, 
  but I wanted to wait and see how the code needs to integrate before I 
  put much time into reworking it.
- found is a defaultdict mapping milestone labels to line indicies,
  where missing keys have the empty list value. Line indicies (as ints) 
  are then appended onto the lists when a milestone is matched. found 
  is the structure returned by check_milestones.
- Class Dispatcher is derived from dict to take advantage of the 
  __missing__ method in the dict interfact. Using __missing__ it is 
  possible to catch the key of a missed reference, which defaultdict 
  does not do. For clarity I'd like to change this to instead be a dict 
  or defaultdict instance with __missing__ overloaded, instead of an 
  entire class.
- parse_dispatcher is a Dispatcher dict mapping property keywords to 
  handler methods, where missing keys are dynamically generated methods 
  that print an error and return False. parse_dispatcher is used only 
  in fan_subnodes and could potentially be folded into that method with 
  a closure.
- match_milestone encapsulates the check logic, taking a single 
  milestone expression dictionary and a single log line string and 
  returning True or False. Entry point into fan_subnodes and 
  parse_dispatcher.

Notable methods:
- search_node encapsulates the regex search functionality of re.search. 
  Takes value_parameters, a list of regex strings, and search_content, 
  a string of text to be searched. value_parameters is assumed to be a 
  list to support list nodes in the YAML. Returns True if re.search 
  returned a Match object for any of the given strings in 
  value_parameters, and False if re.search returned None in all cases. 
  By filtering the content of a log line string, search_node can be 
  used to implement both input and output checking. parse_input and 
  parse_output are responsible for preparing the parameters for 
  search_node. If we need to support search options such as match 
  strictness, those parameters can be caught and interpreted here or in 
  parse_input/parse_output.
- 
    


"""

