import sys
from milestone import yield_csv
from regex import search

if __name__ == '__main__':
  for line in yield_csv(sys.argv[1]):
    print(line)
    print(search(r'{e}(?b)(?:batz)', line[0]))