import re
import sys
import os
import csv
import random
import string


def prepend_edurange(csvwriter):
    headers = ["INPUT|null|A0 M0 T0|null|null|MS: Find Home Dir \l Accepted Commands: \l pwd \l Accepted Options: \l N/A \l|OUTPUT",
               "INPUT|null|A1 M1 T1|null|null|MS: Read man pwd \l Accepted Commands: \l man \l Accepted Options: \l pwd \l|OUTPUT",
               "INPUT|null|A2 M2 T2|null|null|MS: List Home Dir \l Accepted Commands: \l ls \l Accepted Options: \l N/A \l|OUTPUT",
               "INPUT|null|A3 M3 T3|null|null|MS: Read man ls \l Accepted Commands: \l man \l Accepted Options: \l ls \l|OUTPUT",
               "INPUT|null|A4 M4 T4|null|null|MS: ls long home \l Accepted Commands: \l ls \l Accepted Options: \l -l \l|OUTPUT",
               "INPUT|null|A5 M5 T5|null|null|MS: Change Dir View \l Accepted Commands: \l cd \l Accepted Options: \l view \l|OUTPUT",
               "INPUT|null|A6 M6 T6|null|null|MS: List long view \l Dir: \l /home/$USER/view \l Accepted Commands: \l ls \l Accepted Options: \l -a \l -la \l -al \l|OUTPUT",
               "INPUT|null|A7 M7 T7|null|null|MS: Cd back home \l Accepted Commands: \l cd \l Accepted Options: \l .. \l|OUTPUT",
               "INPUT|null|A8 M8 T8|null|null|MS: ls hidden home \l Dir: \l /home/$USER \l Accepted Commands: \l ls \l Accepted Options: \l -la \l -al \l|OUTPUT",
               "INPUT|null|A9 M9 T9|null|null|MS: Move file1 \l Accepted Commands: \l mv \l Accepted Options: \l file1.txt \l renamed_file1.txt \l|OUTPUT",
               "INPUT|null|A10 M10 T10|null|null|MS: Copy file2 \l Accepted Commands: \l cp \l Accepted Options: \l file2.txt \l copied_file2.txt \l|OUTPUT",
               "INPUT|null|A11 M11 T11|null|null|MS: Copy perm1 \l Accepted Commands: \l cp \l Accepted Options: \l perm1.txt \l copied_perm1.txt \l|OUTPUT",
               "INPUT|null|A12 M12 T12|null|null|MS: Read man chmod \l Accepted Commands: \l man \l Accepted Options: \l chmod \l|OUTPUT",
               "INPUT|null|A13 M13 T13|null|null|MS: Chmod perm1 \l Accepted Commands: \l chmod \l Accepted Options: \l copied_perm1.txt 660 \l|OUTPUT",
               "INPUT|null|A14 M14 T14|null|null|MS: Copy perm2 \l Accepted Commands: \l cp \l Accepted Options: \l perm2.txt \l copied_perm2.txt \l|OUTPUT",
               "INPUT|null|A15 M15 T15|null|null|MS: Chmod perm2 \l Accepted Commands: \l chmod \l Accepted Options: \l copied_perm2.txt 764 \l|OUTPUT"]
    for line in headers:
        csvwriter.writerow([line])


def append_reports_edurange(csvwriter):
    reports = ["INPUT|R|A0 M0||null||OUTPUT",
               "INPUT|R|A1 M1||null||OUTPUT",
               "INPUT|R|A2 M2||null||OUTPUT",
               "INPUT|R|A3 M3||null||OUTPUT",
               "INPUT|R|A4 M4||null||OUTPUT",
               "INPUT|R|A5 M5||null||OUTPUT",
               "INPUT|R|A6 M6||null||OUTPUT",
               "INPUT|R|A7 M7||null||OUTPUT",
               "INPUT|R|A8 M8||null||OUTPUT",
               "INPUT|R|A9 M9||null||OUTPUT",
               "INPUT|R|A10 M10||null||OUTPUT",
               "INPUT|R|A11 M11||null||OUTPUT",
               "INPUT|R|A12 M12||null||OUTPUT",
               "INPUT|R|A13 M13||null||OUTPUT",
               "INPUT|R|A14 M14||null||OUTPUT",
               "INPUT|R|A15 M15||null||OUTPUT"]
    for line in reports:
        csvwriter.writerow([line])


def process_logs(log_dir, completed_milestones):
    for file in os.listdir(log_dir):
        filename = os.fsdecode(file)
        # print(file)
        if filename.endswith(".json"):
            process_kypo(log_dir, filename, completed_milestones)
        elif filename.endswith(".csv"):
            process_edurange(log_dir, filename)


def process_edurange(log_dir, name):
    with open(os.path.join(log_dir, name), 'r') as csv_file:
        reader = list(csv.reader(csv_file))
        for line in reader:
            s_name = ''
            if len(line) < 6:
                continue
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
        print(line)
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
        csvfile = open(os.path.join(out_dir, csv_output_file), 'w', newline='\n', encoding='utf-8')
        csvwriter = csv.writer(csvfile, quotechar='%', escapechar='#', quoting=csv.QUOTE_NONE, )
        prepend_edurange(csvwriter)
        for line in student_logs[s]:
            csvwriter.writerow(line)
        append_reports_edurange(csvwriter)
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
        print("Milestone #{} Dirs:{} Cmds:{} Opts:{}".format(str(i), expected_dirs, expected_cmds, expected_opts))
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

        # Anonymize student usernames
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
                      reader[-1][5][13:]]

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
    csvfile = open(os.path.join(out_dir, csv_output_file), 'w', newline='\n', encoding='utf-8')
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
        print("Milestone #{} Dirs:{} Cmds:{} Opts:{}".format(str(i), expected_dirs, expected_cmds, expected_opts))
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

    # Initialize lists for milestone averages, attempts, and milestone patterns
    milestones = []
    completed_milestones = {}
    log_lines = []
    student_names = []
    allStu = {}
    anon_names = {}

    # Initialize lists to zeroes for each milestone, and load in regex patterns
    with open(milestone_file, 'r', encoding='utf-8-sig') as mFile:
        mNum = 0
        for line in mFile:
            mNum += 1
            milestones.append(line.strip('\n'))
    for m in milestones:
        print(m)

    process_logs(log_dir, completed_milestones)
    print(completed_milestones)
