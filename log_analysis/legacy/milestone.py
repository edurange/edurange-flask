import csv


class LogLine:
    pass


class LogReader(csv):
    def __init__(self, csvfile):
        self.file = open(csvfile, 'r')
        self.data = list(super(csv.reader(self.file)))



class MilestoneList:
    FW_STONES = {1: {"cmds": ["pwd"],
                     "args": [None],
                     "out": ["/home/$USER"],
                     "wdir": ["/home/$USER"]},
                 2: {"cmds": ["man"],
                     "args": ["pwd"],
                     "out": ["*"],
                     "wdir": ["*"]}
                 }

    def __init__(self, name="Default", stones=[]):
        self.scenario_name = name
        self.stones = stones

    def get_stones_by_name(self, scenario_name):
        pass
        if scenario_name == "File Wrangler":
            self.stones.append(Milestone(m) for i, m in enumerate(MilestoneList.FW_STONES))


class Milestone:
    def __init__(self, cmd_pattern=None, arg_pattern=None, out_pattern=None, dir_pattern=None):
        self.__cmd = cmd_pattern
        self.__arg = arg_pattern
        self.__out = out_pattern
        self.__dir = dir_pattern

    @property
    def cmd(self):
        return self.__cmd

    @cmd.setter
    def cmd(self, cmd_pattern):
        print("Using Command Setter")
        if cmd_pattern is None:
            raise ValueError("Command pattern invalid")
        else:
            self.__cmd = cmd_pattern

    @property
    def arg(self):
        return self._arg

    @arg.setter
    def arg(self, arg_pattern):
        if arg_pattern is None:
            raise ValueError("Command pattern invalid")
        else:
            self._arg = arg_pattern

    @property
    def out(self):
        return self._out

    @out.setter
    def out(self, out_pattern):
        if out_pattern is None:
            raise ValueError("Command pattern invalid")
        else:
            self._out = out_pattern

    @property
    def dir(self):
        return self._dir

    @dir.setter
    def dir(self, wdir_pattern):
        if wdir_pattern is None:
            raise ValueError("Command pattern invalid")
        else:
            self._dir = wdir_pattern

    def __eq__(self, other):
        pass
