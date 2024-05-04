import sys
from milestone import yield_csv, remove_null_bytes

if __name__ == '__main__':
  for line in yield_csv(sys.argv[1], filter_f = remove_null_bytes):
    print(line)