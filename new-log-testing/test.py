import re

if __name__ == "__main__":

    stdin_line = "netstat -tunapl | grep 'password'"
    
    desired_arguments = ['a', 't', 'n', 'u', 'p', 'l']
    
    found_command = False
    found_args = False

 
    command_sequence = stdin_line.split("|")

    for c in command_sequence:
        token_sequence = [t for t in c.split(" ") if t != '']
        command = token_sequence[0]
        args = token_sequence[1:] 
        print(args)

        count = 0
        for item in desired_arguments:
            for a in args:
                if item in a:
                    count += 1

        print(count)
               

    args = ""

