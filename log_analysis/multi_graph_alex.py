#!/usr/bin/env python
# testing directed graphs with separate
# .dot files for each users
# b3rp
# 3/6/19

import sys
import csv
from graphviz import Digraph


def graph_create(user, commands):
    graph = Digraph(node_attr={'shape': 'box'}, comment="creating graph for user: {}".format(user))
    for j in range(0, len(commands[user])):
        graph.node(str(j), commands[user][j])
    for j in range(1, len(commands[user])):
        graph.edge(str(j - 1), str(j), constraint='false')
    graph.attr(rankdir='LR')
    # print(graph.source)
    graph.render('strace-output/' + user + '_graph.dot')


def main():
    with open('strace-example.csv', 'r') as csv_file:

        testreader = reversed(list(csv.reader(csv_file, delimiter=',')))
        commands = {}
        hourTime = ""
        for row in testreader:
            if len(row) > 0:
                if row[0] == 'performed_at':
                    pass
                else:
                    hourTime = row[0].split()[1]
                user_name = row[4]
                # user_dir = row[0].split(":")[-1]
                if user_name not in commands.keys():
                    commands[user_name] = []
                    commands[user_name].append('{} {}'.format(hourTime, row[6]) if len(user_name) > 0 else row[4])
                else:
                    commands[user_name].append('{} {}'.format(hourTime, row[6]) if len(user_name) > 0 else [row[4]])

    for key in commands.keys():
        user = key
        print(user)
        print(commands)
        graph_create(user, commands)


if __name__ == "__main__":
    main()
