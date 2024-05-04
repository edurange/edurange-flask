import sys
from milestone import load_milestones

if __name__ == '__main__':
  for value in load_milestones(sys.argv[1]):
    print(value)