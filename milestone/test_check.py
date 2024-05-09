import sys
from milestone import load_milestones, toy_yield_log, milestone_tagger

def result_summary(results):
  """
  For a list of confidence rankings and interpreter traces, returns a 
  list with just the confidence ranking and the 'label' field from the 
  milestone trace
  """
  return [(rank, trace['label']) for rank, trace in results]

if __name__ == '__main__':
  milestones_deserialized = load_milestones(sys.argv[1])
  print(milestones_deserialized)
  print('-------')
  log_iterable = enumerate(toy_yield_log(sys.argv[2]))
  final_matches = {}
  final_results = []
  for matched, results in milestone_tagger(milestones_deserialized,
                                        log_iterable):
    print('-------')
    print(matched)
    for result in result_summary(results):
      print(result)
    final_matches = matched
    final_results = results
  print('-------')
  print(final_matches)
    