import sys
from milestone import load_milestones, toy_yield_log, milestone_tagger

if __name__ == '__main__':
  milestones_deserialized = load_milestones(sys.argv[1])
  print(milestones_deserialized)
  
  log_iterable = enumerate(toy_yield_log(sys.argv[2]))
  print(log_iterable)
  
  for found in milestone_tagger(milestones_deserialized, log_iterable):
    print(found)