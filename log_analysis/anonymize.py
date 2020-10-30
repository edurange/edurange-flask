import sys
import os
import csv
import hashlib


def anonymize(histfile):
    reader = list(csv.reader(histfile))
    for row in reader:
        out_row = []
        if len(row) >= 3:
            if len(row[3].split('/')) >= 3:
                user = row[3].split('/')[2]
                if user not in students.keys():
                    hashed_name = hashlib.md5(user.encode())
                    students[user] = hashed_name.hexdigest()[:6]
            for col in row:
                out_col = col
                for user in students.keys():
                    if user in col:
                        out_col = out_col.replace(user, students[user])
                out_row.append(out_col)
            out_lines.append(out_row)
    new_filename = filename.split('.')[0] + "-anon" + ".csv"
    with open(os.path.join(out_dir, new_filename), 'w', encoding='latin1') as csv_out:
        csvwriter = csv.writer(csv_out, delimiter=',')
        for line in out_lines:
            csvwriter.writerow(line)


if __name__ == '__main__':
    log_dir = sys.argv[1]
    out_dir = sys.argv[2]
    for file in os.listdir(log_dir):
        out_lines = []
        filename = os.fsdecode(file)
        students = {}
        with open(os.path.join(log_dir, filename), 'r', encoding='latin1') as csv_file:
            anonymize(csv_file)
    print("Success")
