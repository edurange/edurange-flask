import sys
from milestone import load_milestones, toy_yield_log, \
                      milestone_tagger, yield_stdin

def result_summary(results):
  """
  For a list of confidence rankings and interpreter traces, returns a 
  list with just the confidence ranking and the 'label' field from the 
  milestone trace
  """
  return [(rank, trace['label']) for rank, trace in results]

def print_and_yield(iterator):
  """Wrap an iterator to print what it yields"""
  for obj in iterator:
    print(obj)
    yield obj

if __name__ == '__main__':
  milestones_deserialized = load_milestones(sys.argv[1])
  print(milestones_deserialized)
  print('-------')
  log_iterable = print_and_yield(toy_yield_log(yield_stdin()))
  final_matches = {}
  final_results = []
  for matched, results in milestone_tagger(milestones_deserialized,
                                            log_iterable):
    print('-------')
    print(matched)
    print('--- Results:')
    for result in result_summary(results):
      print(result)
    final_matches = matched
    final_results = results
    print('-------')
  print('-------')
  print(final_matches)
    