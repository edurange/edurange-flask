'''
    Prototype:
      - Label: M1
        Type: Input
        Objective: Long listing in the home directory
        Command: ls
        Args: -la
        Strictness: FullMatch
      - Label: M2
        Type: Output
        Objective: Read the secret file
        Output: "sup3rs3cr3t"
        Strictness: FullMatch
      - Label: M3
        Type: Compound
        Objective: Listing and Read Secret
        Requirements: M1, M2
'''


class Milestone:
    def __init__(self):
        self.label = "M1"
        self.mtype = ""
        self.objective = ""
        self.command = ""
        self.args = ""
        self.strictness = ""

    def match(self):
        raise NotImplementedError()


class MilestoneInput(Milestone):
    def match(self, csv_line):
        return csv_line[4]


reader = csv.reader(csvFile, delimiter=',', quotechar='%', quoting=csv.QUOTE_MINIMAL)
csv = open("untagged.csv", "r")
data = csv.readlines()
csv.close()

test = Milestone()
input_milestone = MilestoneInput()

input_milestone.match(data[0])
