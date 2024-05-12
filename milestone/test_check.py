import sys
from milestone import load_milestones, toy_yield_log, \
                      milestone_tagger

def result_summary(results):
  """
  For a list of confidence rankings and interpreter traces, returns a 
  list with just the confidence ranking and the 'label' field from the 
  milestone trace
  """
  return [(rank, trace['label']) for rank, trace in results]

def append_ranks_to_output(line):
  """
  For a line yielded by milestone_tagger, returns a list with the 
  confidence ranks of each milestone appended to the original_text list 
  from csv.reader, ready to be written back out.
  """
  _, results, original_text = line
  return original_text.copy() + [rank for rank, _ in results]

def print_and_yield(iterator):
  """Wrap an iterator to print what it yields"""
  for obj in iterator:
    print('print_and_yield')
    print(obj)
    yield obj

if __name__ == '__main__':
  milestones_deserialized = load_milestones(sys.argv[1])
  print(milestones_deserialized)
  print('-------')
  log_iterable = print_and_yield(toy_yield_log(sys.stdin))
  final_matches = {}
  final_results = []
  for line in milestone_tagger(milestones_deserialized, log_iterable):
    matched, results, original_text = line
    print('-------')
    print(matched)
    print('--- Results:')
    for rank, label in result_summary(results):
      print(rank, label)
    final_matches = matched
    final_results = results
    print('-------')
    print(append_ranks_to_output(line))
  print('-------')
  print(final_matches)
    