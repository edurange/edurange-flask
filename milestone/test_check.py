import sys
from milestone import load_milestones, yield_log

  milestones_deserialized = load_milestones('milestones.yml')
  print(milestones_deserialized)
  
  log_stream = enumerate(yield_log('log.csv'))
  print(log_stream)
  
  for found in check_milestones(milestones_deserialized, log_stream):
    print(found)