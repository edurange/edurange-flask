import sys
from milestone import relative_search

if __name__ == '__main__':
  pattern = 'foo | bar'
  print(sys.argv)
  print(len(sys.argv))
  text = sys.argv[1]
  print(relative_search(pattern, text))