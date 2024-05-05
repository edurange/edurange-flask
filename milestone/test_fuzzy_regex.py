import sys
from milestone import yield_csv
from regex import search

if __name__ == '__main__':
  search_string = "batz"
  pattern = f'(?:{search_string})' + r'{e}(?b)'
  # Is f'(?:{search_string}){"{e}"}(?b)' clearer?
  for line in yield_csv(sys.argv[1]):
    print(line)
    print(search(pattern, line[0]))
    print(search(pattern, line[0]).match)