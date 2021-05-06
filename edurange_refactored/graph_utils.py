import os


def getGraph(s, username): # s - scenario name, username - student username
    try:
        graph = open("./data/tmp/" + s + "/graphs/" + username + ".svg", "r").read()
        return graph
    except:
        return None


def getLogFile(s): # s - scenario name
    logs = "./data/tmp/" + s + "/" + s + "-history.csv"
    if os.path.isfile(logs):
        logs = "." + logs
        return logs
    else:
        return None
