import sys
import subprocess
import time
import os
import os.path

def find_ports(u,port_list):        #finds ports that user is on so message is sent to all of them
    s = subprocess.check_output(['who'])
    for w in s.splitlines():
        temp = w.split()
        if temp[0].decode("utf-8") == u:            
            port_list.append(temp[1].decode("utf-8"))

def levenshtein(s, t):            #checks similarities between two words
    rows = len(s) + 1
    cols = len(t) + 1
    deletes = 1
    inserts = 1
    substitutes = 1
    dist = [[0 for x in range(cols)] for x in range(rows)]

    for row in range(1,rows):
        dist[row][0] = row * deletes
    for col in range(1, cols):
        dist[0][col] = col * inserts
    for col in range(1,cols):
        for row in range(1,rows):
            if s[row-1] == t[col-1]:
                cost = 0
            else:
                cost = substitutes
            dist[row][col] = min(dist[row-1][col] + deletes, dist[row][col-1] + inserts, dist[row-1][col-1] + cost)
    return dist[row][col]

def follow(filename):                       #continously reads from a file
    current = open(filename, "r")
    curino = os.fstat(current.fileno()).st_ino
    while(True):
        while(True):
            line = current.readline()
            if not line:
                break
            yield line

        try:
            if(os.stat(filename).st_ino != curino):
                new = open(filename, "r")
                current.close()
                current = new
                curino = os.fstat(current.fileno()).st_ino
                continue
        except(IOError):
            pass
        time.sleep(1)

def print_bash(usern,nod,directo): #obtains necessary bash directory to be printed
    folders = directo.split('/')
    trailingMessage = ""
    if usern in folders:
        indexUser = folders.index(usern) + 1
        if indexUser == len(folders):
            trailingMessage = ":~"
        else:
            trailingMessage = ":~" + "/".join(folders[indexUser:])
    else:
        trailingMessage = ":" + directo

    if usern == 'root':
        trailingMessage = trailingMessage + "#"
    else:
        trailingMessage = trailingMessage + "$"
    sys.stdout.write(usern + "@" + nod + trailingMessage + " ")
    sys.stdout.flush()

def read_milestones_messages(filename,numMilestones):
    milestones_output = [[1],[1],[1],[1],[1]]
    if(os.path.isfile(filename)):
        basicMessages =['"Make sure you are running the commands on the adequate node"', '"Double check your commands, something might be misspelled"','"Some parameters might be missing"', '"Adding sudo at the beginning of a command grants you superuser access"', '"Double check your commands, something might be misspelled"']
        milestones_options = ["NO","MS","MP","SD","UN"]
        for y in range(len(milestones_output)):   #populate basic messages matrix
            for x in range(numMilestones):
                milestones_output[y].append('\nHint - ' + basicMessages[y])
        mess_file = open(filename, "r")
        lines = mess_file.readlines()
        for line in lines:
            line_inputs = line.split(',')       #intervention_abbreviation,milestone_index,message
            indexOption = milestones_options.index(line_inputs[0])
            if(int(line_inputs[1]) == -1):
                milestones_output[indexOption][0] = 0
            else:
                milestones_output[indexOption][int(line_inputs[1])+1] = '\nHint - ' + line.split(',',2)[2].splitlines()[0]
        return milestones_output
    return [[0],[0],[0],[0],[0]]


def main():
    if(len(sys.argv) < 4):
        sys.exit("Provide user_file, milestone_file, and milestones_messages\ne.g. python intervention.py ./tester1.txt milestones-synflood milestones-messages")
    loglines = follow(sys.argv[1])      #implements continous intervention from file

    f_mil = open(sys.argv[2]) #open milestones file
    if f_mil.mode != 'r':
        sys.exit("Error with the milestones file")
    milestones = []
    mil = f_mil.readlines()
    for x in mil: #read milestones file and put them inside a list to be later used for comparison
        milestones.append(x)
    mistakes_mtx = [[0 for i in range(4)] for j in range(len(milestones))] #mastakes_mtx[x][0] is for wrong parameters
    for j in mistakes_mtx:                                                  #mistakes_mtx[x][1] for mispelled parameters
        j[2] = [0] * 5                                                      #mistakes_mtx[x][2] for node
                                                                             #mistakes_mtx[x][3] for index command number of node
    sudoCounter = 0
    flagSudo = 0
    userNode = ""
    username = ""
    userDirectory = ""

    intervent_milestones = read_milestones_messages(sys.argv[3], len(milestones))
    checkNode = intervent_milestones[0]           #NO - Worng Node
    checkMisspelling = intervent_milestones[1]    #MS - Mispelling
    checkMissCommand = intervent_milestones[2]    #MP - MIssing Parameters
    checkSudo = intervent_milestones[3]           #SD - Sudo Permission
    checkUndef = intervent_milestones[4]          #UN - Check undefined
    
    for y in loglines: #iterates through the file
        sections = y.split("|")                         #the sections refer to the informtion between the | in the input file
        if "denied" in y and flagSudo != 1 and sections[0] != "INPUT" and checkSudo[0] == 1:
            flagSudo = 1
            sudoCounter = sudoCounter + 1
            if sudoCounter == 3:
                proc = subprocess.Popen(['sudo','echo','-e',checkSudo[1]])
                proc.communicate()
                print_bash(username,userNode,userDirectory)
                sudoCounter = 0

        if sections[0] != "INPUT":                     #checks if input line since some of the output might me in multiple lines
            continue
        elif len(sections) < 5:
            continue
        elif "denied" in y and checkSudo[0] == 1:          #checks if denied
            flagSudo = 1
            sudoCounter = sudoCounter + 1
            if sudoCounter == 3:                        #send message and reset counter
                proc = subprocess.Popen(['sudo','echo','-e',checkSudo[1]])
                proc.communicate()
                print_bash(username,userNode,userDirectory)
                sudoCounter = 0
        elif flagSudo == 0:
            sudoCounter = 0
        else:
            flagSudo = 0

        for j in mistakes_mtx:                          #implementation of incorrect mode is different than mispelling or missing param
            j[2][j[3]] = 0                              #if three of the last 5 commands show wrong node then send message to user
                                                        #mistakes[x][2] = [0,0,0,0,0] where each index represent one of the last 5 commands
                                                        #if wrong node appear then we cahnge a value of the list to 1
                                                        #before we check if the command is on the wrong node we set it back to 0
                                                        #j[3] holds the index we are currently on from 0-4


        userNode = sections[6].split(':')[0]                      #gets current node and username
        username = sections[4]
        userDirectory = sections[5]

        if sections[2][0] == "M":                     #if milestone met then no need to analize, update mistakes matrix
            for j in mistakes_mtx:
                j[0] = 0
                j[1] = 0
                j[3] = (j[3] + 1) % 5
            flagSudo = 1
            sudoCounter = 0
            continue
        dividedCommands = sections[6].split(':')[1].split()       #gets commands and the attemps that fall under the command
        multiple_attempts = sections[2].split('A')
        flagNodeSent = 0
        flagParamSent = 0
        flagMisspSent = 0
        flagUndefined = 0
        fgMissp = 0
        flagSendMisspMessage = 0
        if "U" in multiple_attempts[0]:                             #if undefined command check if it is misspelled
            for ind,tmp_mil in enumerate(milestones):
                posInp = tmp_mil.split(',')[1].split('|')
                for pI in posInp:
                    comm = set(pI.split())
                    for userCom in dividedCommands:
                        for com in comm:
                            resLev = levenshtein(userCom,com)
                            if resLev == 1 and fgMissp != 1:
                                mistakes_mtx[ind][1] = mistakes_mtx[ind][1] + 1
                                if mistakes_mtx[ind][1] == 4:
                                    fgMissp = 1
                if fgMissp == 1:
                    mistakes_mtx[ind][1] = 0
                    flagSendMisspMessage = 1
            if flagSendMisspMessage == 1 and checkUndef[0] == 1:         #send message if multiple misspelling
                proc = subprocess.Popen(['sudo','echo','-e',checkUndef[1]])
                proc.communicate()
                print_bash(username,userNode,userDirectory)

        for z in multiple_attempts[1:]:                 #iterates through the attempts tagged
            w = z[0]
            flagMissp = 0
            flagMisParameters = 0
            temp_mil = milestones[int(w)]
            node = temp_mil.split(',')[0]               #required node
            possInputs = temp_mil.split(',')[1].split('|') #multiple routes can be taken to complete a milestone
            if node != userNode and node != '*': #checks if correct node is used
                mistakes_mtx[int(w)][2][mistakes_mtx[int(w)][3]] = 1 #set value of current command as 1 for incorrect node
                if mistakes_mtx[int(w)][2].count(1) == 3: #checks if 5 prev commands list containts three 1s, if it does then notify user
                    if flagNodeSent != 1 and checkNode[0] == 1:
                        flagNodeSent = 1
                        proc = subprocess.Popen(['sudo', 'echo', '-e',checkNode[int(w)+1]])
                        proc.communicate()
                        print_bash(username,userNode,userDirectory)
                    mistakes_mtx[int(w)][2] = [0] * 5
                    mistakes_mtx[int(w)][3] = 0
            
            correctCommands = 0 #maintans count of commands to see if user input them correclty
            for possI in possInputs:
                commands = set(possI.split())
                for userCommand in dividedCommands:
                    if userCommand in commands:     #checks if the user input matches the possible values
                        correctCommands = correctCommands + 1
                    else:
                        for com in commands: #if user command does not match see if it is mispelled 
                            if com in userCommand:
                                correctCommands = correctCommands + 1
                            elif levenshtein(userCommand, com) == 1:
                                correctCommands = correctCommands + 1
                                flagMissp = 1
                    if flagUndefined == 1 and flagMissp != 1:
                        flagUndefined = 2
                        for com in commands:
                            if levenshtein(userCommand,com) == 1:
                                flagMissp = 1
                if correctCommands > 0 and correctCommands < len(commands): #if not all commands are met then there are missing commands
                    flagMisParameters = 1
                if correctCommands > 0: #multiple ways to get t a milestone, if correct commands have been dounf then the method used was found
                    break

            if flagMisParameters == 1: #update count of how many commands have been missing paramenters
                mistakes_mtx[int(w)][0] = mistakes_mtx[int(w)][0] + 1
                if mistakes_mtx[int(w)][0] == 3:    #if last three commands are missing param send message and reset
                    mistakes_mtx[int(w)][0] = 0
                    if flagParamSent != 1 and checkMissCommand[0] == 1:
                        flagParamSent = 1
                        proc = subprocess.Popen(['sudo','echo','-e',checkMissCommand[int(w)+1]])
                        proc.communicate()
                        print_bash(username,userNode,userDirectory)
            else:
                mistakes_mtx[int(w)][0] = 0

            if flagMissp == 1:  #update count of mispelled parameters
                mistakes_mtx[int(w)][1] = mistakes_mtx[int(w)][1] + 1
                if mistakes_mtx[int(w)][1] == 4: #sends message if last 4 commands were mispelled
                    mistakes_mtx[int(w)][1] = 0
                    if flagMisspSent != 1 and checkMisspelling[0] == 1:
                        flagMisspSent = 1
                        proc = subprocess.Popen(['sudo', 'echo', '-e',checkMisspelling[int(w)+1]])
                        proc.communicate()
                        print_bash(username,userNode,userDirectory)

            else:
                mistakes_mtx[int(w)][1] = 0
        flagNodeSent = 0
        flagParamSent = 0
        flagMisspSent = 0

        for j in mistakes_mtx:
            for h in j[:2]:
                if h > 0:
                    h = h - 1
            j[3] = (j[3] + 1) % 5

main()
