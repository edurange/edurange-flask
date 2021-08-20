"""Visualization tool for edurange. This creates tool creates a graph of user behavior."""

#written by Aubrey Birdwell in Fall 2020
#for the EduRange project
#aubrey.birdwell@gmail.com

#old imports
#import libs
#import avro
#import csv
import sys
import pygraphviz as pgv
import csv_graph_utility


class Node:
    """
    Node class to be a vertice in a graph of user log data

    Attributes
    ----------
    left : node
    right : node
    data : log entry object

    Methods
    -------
    ...todo
    """
    def __init__(self, data):
        """
        Constructs a node.

        Parameters
        ----------
        data : log entry object
        """
        self.left = None
        self.right = None
        self.data = data


    def insert_right(self, data):
        """
        Inserts a node on the right side of a node.

        Parameters
        ----------
        data : log entry object
        """
        if self.data:
            if self.right is None:
                self.right = Node(data)
            else:
                self.right.insert_right(data)
        else:
            self.data = data
            #print(str(self.data[0]) + " -> " + str(data[0]))


    def insert_left(self, data):
        """
        Inserts a node on the left side of a node.

        Parameters
        ----------
        data : log entry object
        """
        #Compare the new milestone with template and branch left
        if self.data:
            if (self.right is not None and data[2] not in self.data[2]):
                self.right.insert_left(data)
            else:
                if self.left is not None:
                    self.left.insert_left(data)
                else:
                    self.left = Node(data)


    def insert_left_report(self, data):
        """
        Inserts a special report node object on the left.

        Parameters
        ----------
        data : log entry object (includes info about success / failures)
        """
        #Compare the new milestone with template and branch left
        if self.data:
            if(self.right is not None and data[2] not in self.data[2]):
                self.right.insert_left_report(data)
            else:
                if self.left is not None:
                    if ('A' in data[2] and 'M' in data[2]):
                        if 'A' in self.data[2]:
                            if data[3] == 'None':
                                data[3] = 'A'
                            else:
                                data[3] += 'A'
                            self.left.insert_left_report(data)
                        elif 'M' in self.data[2]:
                            if data[3] == 'None':
                                data[3] = 'M'
                            else:
                                data[3] += 'M'
                            self.left.insert_left_report(data)
                        else:
                            print('error line 97')
                    else:
                        #advance one left node if not a report node
                        self.left.insert_left_report(data)
                else:
                    #end of the line
                    self.left = Node(data)

    def in_order_traverse(self):
        """
        Simplified example of traversal for debugging.

        Parameters
        ----------
        None
        """
        if self.left:
            self.left.in_order_traverse()
        try:
            if 'U' in self.data[2]:
                print(self.data)
        except IndexError:
            print('Exception located here:')
            print(self.data)
        if self.right:
            self.right.in_order_traverse()

    def label_nodes(self):
        """
        Traverses and labels vertices/nodes for graphviz.

        Parameters
        ----------
        None
        """
        if self.left:
            self.left.label_nodes()
        try:
            if 'T' in self.data[2]:
                text = str(self.data[4])
                # print graph viz code to console for debugging
                # print(str(self.data[0]) + "[label= " + text + ',
                # shape = box3d, style="filled", fillcolor="white", fontcolor="black"]')

                G.add_node(self.data[0], label=self.data[4], shape='box3d', \
                           style='filled', fillcolor='white', fontcolor='black')
            elif('M' in self.data[2] and 'A' not in self.data[2]):
                text = 'Milestone: ' + str(self.data[2]) + '\\lCommand used: \\l' \
                    + str(self.data[4]) + '\\lTTY Entry: ' + str(self.data[0]) + '\\l'
                #print graph viz code to console for debugging
                #changing the color to green 3 from green 1
                #print(str(self.data[0]) + '[label= ' + text + ', shape = rectangle,
                #style="filled", fillcolor="green", fontcolor="black"]')
                G.add_node(self.data[0], label=text, shape='rectangle', \
                           style='filled', fillcolor='green3', fontcolor='black')
            elif('A' in self.data[2] and 'M' not in self.data[2]):
                text = 'Milestone: ' + str(self.data[2]) + '\\lCommand used: \\l' \
                    + str(self.data[4]) + '\\lTTY Entry: ' + str(self.data[0]) + '\\l'
                #print graph viz code to console for debugging
                #print(str(self.data[0]) + '[label= ' + text + ', shape = rectangle,
                #style="filled", fillcolor="yellow", fontcolor="black"]')
                # changed color from yellow to gold2
                G.add_node(self.data[0], label=text, shape='rectangle', \
                           style='filled', fillcolor='gold2', fontcolor='black')

            else:

                #could really use some work here. Then again maybe it's fine.
                attempts = len(self.data[3])
                if('A' not in self.data[3] and 'M' not in self.data[3]):
                    complete = 'no'
                    # old color red new color firebrick
                    #color = 'red'
                    color = 'firebrick3'
                    attempts = 0
                elif 'M' in self.data[3]:
                    complete = 'yes'
                    #color = 'chartreuse3'
                    color = 'green3'
                else:
                    complete = 'maybe'
                    #color = 'orange'
                    color = 'orange1'
                text = 'Report: ' + str(self.data[2]) + '\\l# attempts: ' \
                    + str(attempts) + '\\lCompleted: ' + complete + '\\l' + str(self.data[3]) + '\\l'
                #print graphviz code to console for debugging
                #print(str(self.data[0]) + "[label= " + text+ ', shape = oval,
                #style="filled" fillcolor=' + color + ', fontcolor="black"]')
                G.add_node(self.data[0], label=text, shape='oval', \
                           style='filled', fillcolor=color, fontcolor='black')
        except IndexError:
            print('Exception located here:')
            print(self.data)
        if self.right:
            self.right.label_nodes()

    def label_edges(self):
        """
        Traverses and labels edges for graphviz.

        Parameters
        ----------
        None
        """
        if self.left:
            self.left.label_edges()
        try:
            if self.left:
                G.add_edge(self.data[0], self.left.data[0], label='', penwidth='2')
                #print graphviz code to console for debugging
                #print(str(self.data[0]) + "->" + str(self.left.data[0]))
        except IndexError:
            print('Exception located here:')
            print(self.data)
        if self.right:
            self.right.label_edges()

    def print_tree(self):
        """
        Prints tree information for debugging.

        Parameters
        ----------
        None
        """
        if self.left:
            self.left.print_tree()
        print(self.data)
        if self.right:
            self.right.print_tree()



# outputs graphviz file
def output_graph(output_dir):
    """
    Outputs a graphviz file (svg).

    Parameters
    ----------
    Output directory.
    """
    #import pygraphviz as pgv
    #print graphviz code to console for debugging
    #print("digraph edurange {")
    #print()
    #print("node [shape=rectangle fontname=\"Helvetica\"];")
    #print()
    #G = pgv.AGraph(strict=False, directed=True)
    #this needs to be dealt with... count up the milestone nodes to derive this following line...
    #print("{rank=same; 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 -> 8 -> 9 ->
    #10 -> 11 -> 12 -> 13 -> 14 -> 15 -> 16 [style=invis]}")

    G.graph_attr['rankdir'] = 'UD'
    G.node_attr['shape'] = 'box'

    root.label_nodes()
    #print("# end labelling of nodes")
    root.label_edges()

    #print graphviz code to console for debug
    #print()
    #print("}")

    #notes on use of this function:
    ###draw(path=None,format=None,prog=None,args='')
    G.draw((output_dir + 'graph.svg'), prog='dot')



if __name__ == "__main__":

    #proper arg check
    if len(sys.argv) != 3:
        print('usage:\n graph_report.py <file_to_graph> <out_dir>')
        sys.exit(1)

    file_label = sys.argv[1]
    out_dir = sys.argv[2]

    G = pgv.AGraph(strict=False, directed=True)

    #call file loader function
    log = csv_graph_utility.file_load(file_label)

    root = Node(log[0])
    for i in range(1, len(log)):
        try:
            if 'U' not in log[i][2]:
                if 'T' in log[i][2]:
                    #print("Inserting right " + "node: " + str(log[i][2]))
                    root.insert_right(log[i])
                elif 'T' not in log[i][2]:
                    #print("Inserting left " + "node: " + str(log[i][2]))
                    root.insert_left_report(log[i])
        except IndexError:
            print('Exception located here:')
            print(log[i])
    #print()
    output_graph(out_dir)
