### Author: Aubrey Birdwell
### emergency script to separate csv dump of users log data

import csv
import sys

if __name__ == "__main__":

    #proper arg check
    if len(sys.argv) != 2:
        print('usage: batch_process_csv.py <file_to_process>')
        sys.exit(1)

    file_label = sys.argv[1]

    csv_file = open(file_label, 'r')
    reader = csv.reader(csv_file, delimiter="|", quotechar="%", quoting=csv.QUOTE_MINIMAL)

    log = dict()

    # csv organization
    # INPUT|uniqueID|class|time|uid|cwd|input|output (trunc)

    for line in reader:
        if len(line) != 8:
            continue
        else:        
            inpt = 'INPUT'
            uid = line[1]
            milestone = line[2].split(' ')[0] #eliminate earlier ms triggers
            timestamp = line[3]
            user = line[4].lower()
            path = line[5]
            command = line[6].split(':')
            output = 'OUTPUT' #line[7]
            if user not in log:
                log[user] = []
            event = (inpt, uid, milestone, timestamp, user, path, command[1], output)
            log[user].append(event)
        
    csv_file.close()

    ## create individual files and make graph

    for user in log:
        user_file = open('./usercsv/' + str(user) + '.csv', 'w')            
        #print(str(user) + "--------------------------------------------------")
        for (inpt, uid, milestone, timestamp, user, path, command, output) in log[user]:
            ln = str(inpt) + '|' + str(uid) + '|' + str(milestone.strip()) + '|' + str(timestamp) + '|' \
            + str(user) + '|' + str(path) + '|' + str(command) + '|' + str(output)
            user_file.write(ln + '\n')
            #print(ln, file=user_file)        
            
        user_file.close()

        ## building controlflow graph        

    F = dict()
    for caseid in log:
        for i in range(0, len(log[caseid])-1):
            ai = log[caseid][i][2]
            aj = log[caseid][i+1][2]
            if ai not in F:
                F[ai] = dict()
            if aj not in F[ai]:
                F[ai][aj] = 0
            F[ai][aj] += 1

    import pygraphviz as pgv
    G = pgv.AGraph(strict=False, directed=True)

    G.graph_attr['rankdir'] = 'LR'
    G.node_attr['shape'] = 'box'
    
    values = [F[ai][aj] for ai in F for aj in F[ai]]
    x_min = min(values)
    x_max = max(values)
    
    y_min = 1.0
    y_max = 5.0

    for ai in F:
        for aj in F[ai]:
            x = F[ai][aj]
            tmp_val = float(x_max-x_min)
            if tmp_val == 0:
                y = y_min + (y_max-y_min) * float(x-x_min) / 0.00001
            else:
                y = y_min + (y_max-y_min) * float(x-x_min) / tmp_val
            G.add_edge(ai, aj, label=x, penwidth=y)

    G.draw('devops_control_flow.png', prog='dot')

