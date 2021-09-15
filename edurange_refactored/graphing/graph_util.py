"""Visualization tool for edurange. This creates tool creates a graph of user behavior."""

#written by Aubrey Birdwell in Fall 2020
#revised in summer 2021
#for the EduRange project
#aubrey.birdwell@gmail.com

import graphviz as gv
#may be needed to debug
#import csv_graph_utility
 

class Report:
    """
    Report class stores a tree of log data
    
    Attributes
    ----------
    G : graphviz object
    root : root node
    log : log stream
    """
    def __init__(self, log):
        #stream of log entries from database
        #contains report and milestone templates
        self.log = log        
        self.root = Node(self.log[0]) 

    def get_graph(self):

        G = gv.Digraph(comment='test log', format='svg')

        for i in range(1, len(self.log)):
            try:
                if 'U' not in self.log[i][2]:
                    if 'T' in self.log[i][2]:                        
                        self.root.insert_right(self.log[i])
                    if 'T' not in self.log[i][2]:
                        if 'A' in self.log[i][2] and 'M' in self.log[i][2]:
                            self.root.insert_left_report(self.log[i])
                        else:
                            self.root.insert_left(self.log[i])
            except IndexError:
                print('Exception located here:')
                print(self.log[i])
        
        #output_graph()
        G = self.root.label_nodes(G)
        G = self.root.label_edges(G)
        return G

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
        if(self.right is not None and data[2] not in self.data[2]):
            self.right.insert_left_report(data)
        elif self.left is not None:
            if 'T' in self.data[2]:
                self.left.insert_left_report(data)                                    
            else:
                if 'A' in self.data[2]:
                    if data[3] == 'None':
                        data[3] = 'A'
                    else:
                        data[3] += 'A'

                if 'M' in self.data[2]:
                    if data[3] == 'None':
                        data[3] = 'M'
                    else:
                        data[3] += 'M'
                #advance one left node if not a report node
                self.left.insert_left_report(data)                        
        else:
            #have to have this again for the final case
            #where report is attached to end of tree
            if 'T' not in self.data[2]:
                if 'A' in self.data[2]:
                    if data[3] == 'None':
                        data[3] = 'A'
                    else:
                        data[3] += 'A'

                if 'M' in self.data[2]:
                    if data[3] == 'None':
                        data[3] = 'M'
                    else:
                        data[3] += 'M'
                    #end of the line
            self.left = Node(data)
            

                    
    def label_nodes(self, G):
        """
        Traverses and labels vertices/nodes for graphviz.

        Parameters
        ----------
        None
        """
        
        if self.left:
            self.left.label_nodes(G)
        try:
            if 'T' in self.data[2]:
                text = str(self.data[4])
                G.node(str(self.data[0]), label=self.data[4], shape='box3d', \
                           style='filled', fillcolor='white', fontcolor='black')
            elif('M' in self.data[2] and 'A' not in self.data[2]):
                text = 'Milestone: ' + str(self.data[2]) + '\\lCommand used: \\l' \
                    + str(self.data[4]) + '\\lTTY Entry: ' + str(self.data[0]) + '\\l'                
                G.node(str(self.data[0]), label=text, shape='rectangle', \
                           style='filled', fillcolor='green3', fontcolor='black')
            elif('A' in self.data[2] and 'M' not in self.data[2]):
                text = 'Milestone: ' + str(self.data[2]) + '\\lCommand used: \\l' \
                    + str(self.data[4]) + '\\lTTY Entry: ' + str(self.data[0]) + '\\l'
                G.node(str(self.data[0]), label=text, shape='rectangle', \
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

                if 'M' in self.data[3]:
                    complete = 'yes'
                    #color = 'chartreuse3'
                    color = 'green3'
                else:
                    complete = 'maybe'
                    #color = 'orange'
                    color = 'orange1'
                #can add + str(self.data[3]) + to node for debugging
                text = 'Report: ' + str(self.data[2]) + '\\l# attempts: ' \
                    + str(attempts) + '\\lCompleted: ' + complete + '\\l'
                G.node(str(self.data[0]), label=text, shape='oval', \
                           style='filled', fillcolor=color, fontcolor='black')
        except IndexError:
            print('Exception located here:')
            print(self.data)
        if self.right:
            self.right.label_nodes(G)

        return G
            
            
    def label_edges(self, G):
        """
        Traverses and labels edges for graphviz.

        Parameters
        ----------
        None
        """
        
        if self.left:
            self.left.label_edges(G)
        try:
            if self.left:
                G.edge(str(self.data[0]), str(self.left.data[0]), label='', penwidth='2')                
        except IndexError:
            print('Exception located here:')
            print(self.data)
        if self.right:
            self.right.label_edges(G)
        return G

    def print_tree(self):
        """
        Prints tree information for debugging.

        Parameters
        ----------
        None
        """
        #this method is a backup test method
        if self.left:
            self.left.print_tree()
        print(self.data)
        if self.right:
            self.right.print_tree()

# this may be used to debug
# in order to do so you must modify the csv_graph... util file paths for not flask...
#if __name__ == "__main__":            
#    file_name = "sample_data.csv"
#    log = csv_graph_utility.file_load("sample_data.csv")

#    R = Report(log)
#    G = R.get_graph()
