import sys

from milestone import yield_csv, yield_log, toy_yield_log

if __name__ == '__main__':
  for line in toy_yield_log(sys.argv[1]):
    print(line)