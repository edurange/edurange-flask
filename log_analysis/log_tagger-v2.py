import re
import sys
import os
import csv
import random
import string

def process_logs(log_dir, completed_milestones):
    for file in os.listdir(log_dir):
        filename = os.fsdecode(file)
        #print(file)
        if filename.endswith(".json"):
            process_kypo(log_dir, filename, completed_milestones)
        elif filename.endswith(".csv"):
            process_edurange(log_dir, filename)

def process_edurange(log_dir, name):
    with open(os.path.join(log_dir, name), 'r') as csv_file:
        reader = list(csv.reader(csv_file))
        for line in reader:
            s_name = ''
            try:
                prompt_index = line[6].index('@')
                s_name = line[6][:prompt_index]
            except ValueError:
                try:
                    prompt_index = line[5].index('@')
                    s_name = line[5][:prompt_index]
                except ValueError:
                    print("Mega bad line: {}".format(line))
            if s_name not in student_names and s_name != 'UNKNOWN USER':
                student_names.append(s_name)

            log_lines.append(line)

    student_logs = {}
    for s in student_names:
        student_logs[s] = []
        student_logs[s + '_count'] = 0
        completed_milestones[s] = []
        for m in milestones:
            completed_milestones[s].append(0)

    for line in log_lines:
        timestamp = line[2]
        current_dir = line[3]
        stdin = line[4]
        output = line[5]
        s_name = ''
        try:
            prompt_index = line[6].index('@')

            s_name = line[6][:prompt_index]
        except ValueError:
            try:
                prompt_index = line[5].index('@')
                s_name = line[5][:prompt_index]
            except ValueError:
                print("Mega bad line: {}".format(line))

        if s_name == 'UNKNOWN_USER' or s_name == '':
            print("Skipping Line: {}".format(line))
            continue

        tag = check_milestones_edurange(current_dir, stdin, output, completed_milestones, s_name)

        new_line = ["INPUT|" + s_name + "--" + str(student_logs[s_name + '_count']) + \
                    "|" + tag + "|" + timestamp + "|" + s_name + \
                    "|" + stdin + "|OUTPUT|" + current_dir]

        student_logs[s_name + '_count'] += 1
        student_logs[s_name].append(new_line)

    for s in student_names:
        csv_output_file = s + '.csv'
        csvfile = open(os.path.join(out_dir, csv_output_file), 'w', newline='\n',encoding='utf-8')
        csvwriter = csv.writer(csvfile, quotechar='%', escapechar='#', quoting=csv.QUOTE_NONE, )
        for line in student_logs[s]:
            csvwriter.writerow(line)

        csvfile.close()

    pass

def check_milestones_edurange(working_dir, stdin, stdout, completed_milestones, student):
    tag = ''

    stdin = stdin.split(' ')

    for i, m in enumerate(milestones):
        found_wdir = False
        found_cmd = False
        found_opt = False
        found_output = False
        # if completed_milestones[student][i] == 1:
        #     continue

        mStoneFields = m.split(',')
        expected_dirs = mStoneFields[0].split(' ')
        for j, d in enumerate(expected_dirs):
            expected_dirs[j] = d.replace("$USER", student)

        expected_cmds = mStoneFields[1].split('|')[0].split(' ')
        expected_opts = mStoneFields[1].split('|')[1].split(' ')
        expected_out = mStoneFields[2].split(' ')
        print("--------- START MILESTONE --------")
        print("Milestone #{} Dirs:{} Cmds:{} Opts:{}".format(str(i), expected_dirs,expected_cmds, expected_opts))
        print("With wd:{} stdin:{}".format(working_dir, stdin))

        if expected_dirs[0] == "*":
            found_wdir = True
        elif working_dir in expected_dirs:
            found_wdir = True

        for k, cmd in enumerate(stdin):
            if k == 0 or stdin[0] == 'sessions':
                for ec in expected_cmds:
                    if re.fullmatch(ec, cmd):
                        found_cmd = True
            else:
                for eo in expected_opts:
                    if eo == '':
                        continue
                    if re.match(eo, cmd):
                        print("Options Matched: {} - {}".format(eo, cmd))
                        found_opt = True

        if expected_opts[0] == '':
            if len(stdin) == 1:
                print("Expected opts: {}".format(expected_opts))
                print("Stdin: {}".format(stdin))
                found_opt = True

        found_output = True
        print("----- START CHECK -------")
        print("Cmd:{} Opt:{} Wdir:{} Out:{}".format(found_cmd, found_opt, found_wdir, found_output))
        print("-------------")
        if found_cmd and found_opt and found_wdir and found_output:
            if completed_milestones[student][i] == 0:
                tag = "M" + str(i) + " "
                completed_milestones[student][i] = 1
                print("Marked - Completed")
                print("----- END CHECK --------")
                break
            else:
                tag = "V" + str(i)
                print("Marked - Verified")
                print("----- END CHECK --------")
                continue
        elif found_cmd and found_opt and found_output and not found_wdir:
            if completed_milestones[student][i] == 0:
                tag = "A" + str(i)
                print("Marked - ATTEMPT or verify")
                print("----- END CHECK --------")
                continue
            else:
                tag = "V" + str(i)
                print("Marked - Attempt or VERIFY")
                print("----- END CHECK --------")
                continue
        if tag.startswith("M"):
            continue
        elif found_opt and not found_cmd:
            if found_wdir and found_output:
                if tag.startswith("A") or completed_milestones[student][i] == 1:
                    continue
                else:
                    tag = "A" + str(i)
                    print("Marked - Attempted")
                    print("----- END CHECK --------")
                    continue
            else:
                pass
        elif found_cmd and not found_opt:
            if found_wdir and found_output:
                if tag.startswith("A") or completed_milestones[student][i] == 1:
                    continue
                else:
                    tag = "A" + str(i)
                    print("Marked - Attempted")
                    print("----- END CHECK --------")
                    continue
            else:
                pass
        # elif not found_cmd and not found_opt:
        #     if not found_wdir:
        #         if expected_out != "*":
        #             if found_output:
        #                 if tag == '':
        #                     tag = "U" + str(i)
        #                     print("Marked - Unrelated")
        #                     print("----- END CHECK --------")
        #         else:
        #             continue
        #     continue
        else:
            print("Not Marked")
            continue

    if tag == '':
        tag = "U"
    print("------ END LOOP -----")
    return tag

def process_kypo(log_dir, name, completed_milestones):
    with open(os.path.join(log_dir, name), 'r') as csv_file:
        reader = list(csv.reader(csv_file))
        for line in csv_file:
            log_lines.append(line[line.find('{'):])

        #Anonymize student usernames
        user_id = name.split('-')[1]
        anon_names[user_id] = ''
        stuName = ''.join(random.choice(string.ascii_lowercase) for i in range(3))
        anon_names[user_id] = stuName

        completed_milestones[stuName] = []
        for m in milestones:
            completed_milestones[stuName].append(0)

        formatted_lines = []
        first_line = ["User " + user_id + " start time " + \
                      reader[0][5][13:] + \
                      " end " + \
                      reader[-1][5][13:] ]

        formatted_lines.append(first_line)
        for i in range(3):
            formatted_lines.append(["PADDING"])


        for i, line in enumerate(reader):
            stdin = line[8][line[8].index(':') + 1:].replace("\\", "").replace('"', "")
            try:
                workdir = line[11][line[11].index(':') + 1:].replace("\\", "").replace('"', "")
            except (ValueError, IndexError) as e:
                workdir = 'NotFound'
                print("Bad Line: {} Error: {}".format(line, e))
            tag, completed_milestones = check_milestones_kypo(workdir, stdin, milestones, completed_milestones, stuName)
            timestamp = line[5][13:]

            new_line = ["INPUT|" + user_id + "--" + str(i) + \
                        "|" + tag + "|" + timestamp + "|" + user_id + \
                        "|" + stdin + "|OUTPUT"]

            formatted_lines.append(new_line)

    csv_output_file = name[:name.find('.json')] + '.csv'
    csvfile = open(os.path.join(out_dir, csv_output_file), 'w', newline='\n',encoding='utf-8')
    csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_NONE)

    for line in formatted_lines:
        csvwriter.writerow(line)

    csvfile.close()
    return csv_output_file

def check_milestones_kypo(working_dir, stdin, milestones, completed_milestones, student):
    tag = ''

    stdin = stdin.split(' ')

    for i, m in enumerate(milestones):
        found_wdir = False
        found_cmd = False
        found_opt = False
        found_output = False
        if completed_milestones[student][i] == 1:
            continue

        mStoneFields = m.split(',')
        expected_dirs = mStoneFields[0].split(' ')
        for j, d in enumerate(expected_dirs):
            expected_dirs[j] = d.replace("$USER", student)

        expected_cmds = mStoneFields[1].split('|')[0].split(' ')
        expected_opts = mStoneFields[1].split('|')[1].split(' ')
        expected_out = mStoneFields[2].split(' ')
        print("--------- START MILESTONE --------")
        print("Milestone #{} Dirs:{} Cmds:{} Opts:{}".format(str(i), expected_dirs,expected_cmds, expected_opts))
        print("With wd:{} stdin:{}".format(working_dir, stdin))

        if expected_dirs[0] == "*":
            found_wdir = True
        elif working_dir in expected_dirs:
            found_wdir = True

        found_ls = False
        found_python = False
        found_ssh = False
        found_webmin = False
        found_nmap = False
        for k, cmd in enumerate(stdin):
            if cmd == 'ls':
                found_ls = True
            if cmd == 'webmin':
                found_webmin = True
            if k == 0 or stdin[0] == 'sessions' or stdin[0] == 'python':
                for ec in expected_cmds:
                    if re.fullmatch(ec, cmd.replace("'", "")):
                        found_cmd = True
                        if cmd == 'exploit' or cmd == 'run':
                            found_opt = True
                        elif stdin[0] == 'python':
                            found_python = True
                        elif stdin[0] == 'ssh':
                            found_ssh = True
                        elif stdin[0] == 'nmap':
                            found_nmap = True

            for eo in expected_opts:
                if cmd in expected_cmds:
                    continue
                if eo == '':
                    continue
                if eo == '-a':
                    if not found_ls:
                        continue
                    else:
                            found_opt = True
                elif re.match(eo, cmd):
                    print("Options Matched: {} - {}".format(eo, cmd))
                    found_opt = True

        if expected_opts[0] == '':
            if len(stdin) == 1 and stdin[0] != 'ls' and stdin[0] != 'cd':
                print("Expected opts: {}".format(expected_opts))
                print("Stdin: {}".format(stdin))
                found_opt = True

        found_output = True
        print("----- START CHECK -------")
        print("Cmd:{} Opt:{} Wdir:{} Out:{}".format(found_cmd, found_opt, found_wdir, found_output))
        print("-------------")
        if found_cmd and found_opt and found_wdir and found_output:
            if completed_milestones[student][i] == 0:
                tag = "M" + str(i) + " "
                completed_milestones[student][i] = 1
                print("Marked - Completed")
                print("----- END CHECK --------")
                break
            else:
                tag = "V" + str(i)
                print("Marked - Verified")
                print("----- END CHECK --------")
                continue
        elif found_cmd and found_opt and found_output and not found_wdir:
            if completed_milestones[student][i] == 0:
                tag = "A" + str(i)
                print("Marked - ATTEMPT or verify")
                print("----- END CHECK --------")
                continue
            else:
                tag = "V" + str(i)
                print("Marked - Attempt or VERIFY")
                print("----- END CHECK --------")
                continue
        if tag.startswith("M"):
            continue
        elif found_opt and not found_cmd:
            if found_wdir and found_output:
                if tag.startswith("A") or completed_milestones[student][i] == 1:
                    continue
                elif len(stdin) == 1 or found_webmin:
                    continue
                else:
                    tag = "A" + str(i)
                    print("Marked - Attempted")
                    print("----- END CHECK --------")
                    continue
            else:
                pass
        elif found_cmd and not found_opt:
            if found_wdir and found_output:
                if tag.startswith("A") or completed_milestones[student][i] == 1:
                    continue
                elif found_ls or stdin[0] == "cd" or found_python or found_ssh:
                    continue
                elif stdin[0] == "cat":
                    continue
                elif found_nmap:
                    if len(stdin) >= 3:
                        if completed_milestones[student][i] == 0:
                            tag = "M" + str(i) + " "
                            completed_milestones[student][i] = 1
                            print("Marked - Completed")
                            print("----- END CHECK --------")
                            break
                        else:
                            tag = "V" + str(i)
                            print("Marked - Verified")
                            print("----- END CHECK --------")
                            continue
                else:
                    tag = "A" + str(i)
                    print("Marked - Attempted")
                    print("----- END CHECK --------")
                    continue
            else:
                pass
        # elif not found_cmd and not found_opt:
        #     if not found_wdir:
        #         if expected_out != "*":
        #             if found_output:
        #                 if tag == '':
        #                     tag = "U" + str(i)
        #                     print("Marked - Unrelated")
        #                     print("----- END CHECK --------")
        #         else:
        #             continue
        #     continue
        else:
            print("Not Marked")
            continue

    if tag == '':
        tag = "U"
    print("------ END LOOP -----")
    return tag, completed_milestones


if __name__ == "__main__":
    # Proper usage check
    if len(sys.argv) != 4:
        print('usage:\n master_log_tagger.py <log_dir> <milestone_file> <out_dir>')
        exit(1)

    # Read Arguments
    log_dir = sys.argv[1]
    milestone_file = sys.argv[2]
    out_dir = sys.argv[3]
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)

    #Initialize lists for milestone averages, attempts, and milestone patterns
    milestones = []
    completed_milestones = {}
    log_lines = []
    student_names = []
    allStu = {}
    anon_names = {}

    #Initialize lists to zeroes for each milestone, and load in regex patterns
    with open(milestone_file, 'r', encoding='utf-8-sig') as mFile:
        mNum = 0
        for line in mFile:
            mNum += 1
            milestones.append(line.strip('\n'))
    for m in milestones:
        print(m)



    process_logs(log_dir, completed_milestones)
    print(completed_milestones)
