import sys
from milestone import relative_search

if __name__ == '__main__':
  search_string = 'batz'
  pattern = f'(?:{search_string})' + r'{e}(?b)'
  text = sys.argv[1]
  print(relative_search(pattern, text))