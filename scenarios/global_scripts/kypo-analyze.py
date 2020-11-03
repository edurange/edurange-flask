import csv
import operator
import re
import os
import sys

string = 'i think that that that that student wrote there is not that right'
pattern = 'that'

print([match.start() for match in re.finditer(pattern, string)])

def process_files(log_dir, mNum):
    for file in os.listdir(log_dir):
        filename = os.fsdecode(file)
        #print(file)
        if filename.endswith(".json"):
            #print('test')
            reformat_file(filename)
            with open(os.path.join(log_dir, filename), 'r', encoding='latin-1') as csv_file:
                stuName = filename[0:-1]
                if stuName == 'jack3':
                    continue
                process_student(csv_file, stuName, mNum)

    time_spent(allStu)
    calculate_average()
    calculate_variances()

def reformat_file(name):
    with open(os.path.join(log_dir, name), 'r') as csv_file:
        log_lines = []
        reader = list(csv.reader(csv_file))
        for line in csv_file:
            log_lines.append(line[line.find('{'):])

        user_id = name.split('-')[2]

        formatted_lines = []
        first_line = "User " + user_id + " start time " + \
                     reader[0][4][13:] + \
                     " end " + \
                     reader[-1][4][13:]

        formatted_lines.append(first_line)
        for i in range(3):
            formatted_lines.append("PADDING")


        for i, line in enumerate(reader):
            stdin = line[8][line[8].index(':') + 1:].strip("\"")
            tag = check_milestones(stdin, milestones)
            timestamp = line[4][13:]

            new_line = "INPUT|" + user_id + "--" + i + \
                       "|" + tag + "|" + timestamp + "|" + user_id + \
                       "|" + stdin + "|OUTPUT"

            formatted_lines.append(new_line)

        csv_output_file = name[:name.find('.json')] + '.csv'
        csvfile = open(csv_output_file,'w', newline='',encoding='utf-8')
        csvwriter = csv.writer(csvfile, delimiter='|', quoting=csv.QUOTE_MINIMAL)

        for line in formatted_lines:
            csvwriter.writerow(line)

        csvfile.close()


def check_milestones(input, milestones):
    tag = ''
    for i, m in enumerate(milestones):
        if re.match(m, input) is not None:
            if re.fullmatch(m, input) is not None:
                tag += 'M' + i + ' '
            else:
                tag += 'A' + i + ' '
    if tag == '':
        tag = 'U'
    return tag




def process_student(csv_file, student, mNum):
    reader = list(csv.reader(csv_file, delimiter='|'))
    count = 0

    allStu[student] = {}
    allStu[student]['bitvector'] = []
    allStu[student]['started'] = []
    allStu[student]['completed_at'] = {}
    allStu[student]['first_att'] = []
    allStu[student]['att_num'] = []

    for i in range(mNum):
        allStu[student]['bitvector'].append(0)
        allStu[student]['started'].append(0)
        allStu[student]['first_att'].append(0)
        allStu[student]['att_num'].append(0)
        allStu[student]['completed_at'][mNum] = 0

    for row in reader:
        count += 1
        if count == 1:
            allStu[student]['first_att'][0] = row[0].split(' ')[4]
            allStu[student]['first_att'][1] = row[0].split(' ')[6]
        if count <= 3:
            continue
        if len(row) > 3:
            tags = row[2].split(' ')
            if tags[0] == 'U':
                continue
            if len(tags) > 1:
                for tag in tags:
                    if len(tag) > 0:
                        mIndex = int(tag[1:])
                        if allStu[student]['started'][mIndex] == 0:
                            allStu[student]['started'][mIndex] = 1
                        if tag[0] == 'M' and allStu[student]['bitvector'][mIndex] == 0:
                            allStu[student]['bitvector'][mIndex] = 1
                            allStu[student]['completed_at'][mIndex] = int(row[3])
                            allStu[student]['att_num'][mIndex] += 1
                        elif tag[0] == 'A':
                            allStu[student]['att_num'][mIndex] += 1

def time_spent(studentDict):
    for s in studentDict:
        badKeys = []
        for key in allStu[s]['completed_at']:
            if allStu[s]['completed_at'][key] == 0:
                badKeys.append(key)
        for k in badKeys:
            del allStu[s]['completed_at'][k]

        all_stamps = []

        for item in allStu[s]['completed_at'].items():
            all_stamps.append(item)

        all_stamps.sort(key=operator.itemgetter(1))
        durations = []
        for i in range(mNum + 1):
            durations.append(0)

        for i in range(len(all_stamps)):
            if i == 0:
                durations[all_stamps[i][0]] = all_stamps[i][1] - int(allStu[s]['first_att'][0])
            elif i < len(all_stamps) - 1:
                durations[all_stamps[i][0]] = all_stamps[i + 1][1] - all_stamps[i][1]
            else:
                durations[all_stamps[i][0]] = int(allStu[s]['first_att'][1]) - all_stamps[i][1]

        allStu[s]['time_spent'] = durations
        print(s + " : " + str(allStu[s]['time_spent']))

def calculate_average():
    for m in range(mNum):
        count = 0
        sum = 0
        for s in allStu:
            time = allStu[s]['time_spent'][m]
            if time == 0:
                continue
            else:
                count += 1
                sum += time
        if count != 0:
            mAvgs[m] = round(sum/(count * 1.0), 2)

    for m in range(mNum):
        count = 0
        sum = 0
        for s in allStu:
            attempts = allStu[s]['att_num'][m]
            if attempts == 0:
                continue
            else:
                count += 1
                sum += attempts
            if count != 0:
                mAtts[m] = round(sum/(count * 1.0), 2)
    print("AvgAttempts = " + str(mAtts))
    print("AvgTimes = " + str(mAvgs))

def calculate_variances():
    for s in allStu:
        allStu[s]['time_diff'] = []
        allStu[s]
        for x in range(mNum):
            allStu[s]['time_diff'].append(0)

        for i, m in enumerate(allStu[s]['time_spent']):
            if m == 0 or mAvgs[i] == 0:
                continue
            else:
                allStu[s]['time_diff'][i] = round(m - mAvgs[i], 2)

    for s in allStu:
        allStu[s]['att_diff'] = []
        for x in range(mNum):
            allStu[s]['att_diff'].append(0)

        for i, m in enumerate(allStu[s]['att_num']):
            if m == 0 or mAtts[i] == 0:
                continue
            else:
                allStu[s]['att_diff'][i] = round(m - mAtts[i], 2)

    students = []
    for s in allStu:
        students.append(s)
    mStoneTimes = []
    for m in range(len(students)):
        mStoneTimes.append([])
    for i,s in enumerate(allStu):
        for m in range(mNum):
            mStoneTimes[i].append(allStu[s]['time_spent'][m])
    mStoneAtts = []
    for m in range(len(students)):
        mStoneAtts.append([])
    for i,s in enumerate(allStu):
        for m in range(mNum):
            mStoneAtts[i].append(allStu[s]['att_num'][m])

    data = []
    for i, s in enumerate(students):
        for m in range(mNum):
            data.append([s[:3], 'M' + str(m), mStoneTimes[i][m]])

    data2 = []
    for i, s in enumerate(students):
        for m in range(mNum):
            data2.append([s[:3], 'M' + str(m), mStoneAtts[i][m]])

    pd_df = pd.DataFrame(data, columns=['Student', 'Milestone', 'Time'])
    print(pd_df)

    pd_df2 = pd.DataFrame(data2, columns=['Student', 'Milestone', 'Attempts'])

    print(pd_df2)

    pd_df2.to_csv("R_df2.csv", index=True)

    pd_df.to_csv("R_df.csv", index=True)

if __name__ == "__main__":
    # Proper usage check
    # if len(sys.argv) != 4:
    #     print('usage:\n milestone_logger.py <log_dir> <milestone_file> <out_file>')
    #     exit(1)

    # Read Arguments
    print(sys.argv[1])
    log_dir = sys.argv[1]
    milestone_file = sys.argv[2]
    out_file = sys.argv[3]

    mAvgs = []
    mAtts = []
    milestones = []

    with open(milestone_file, 'r') as mFile:
        mNum = 0
        for line in mFile:
            mNum += 1
            mAvgs.append(0)
            mAtts.append(0)
            milestones.append(line)

    allStu = {}


    process_files(log_dir, mNum)
