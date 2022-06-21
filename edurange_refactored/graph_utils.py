import os


def getGraph(s, username): # s - scenario name, username - student username
    try:
        graph = open("./data/tmp/" + s + "/graphs/" + username + ".svg", "r").read()
        return graph
    except:
        return None

