#!/usr/bin/python
# -*- coding: utf-8 -*-

import random

hints = {
    0:[
        "If you\'re lost, `cd` with no arguments takes you back to your home directory",
        "`.` always represents the current directory. `..` always represents the folder a layer above you",
        "Whitespace characters (spaces, tabs, etc.) generally don\'t have an effect on commands outside of arguments",
        "Some commands can be executed on folders other than your current directory, these will take a path as an argument. You can always use `.` to indicate your current directory, or `pwd` and then you can copy the path",
        "`/` (the root of the file system) is different from `/root` (the root folder)",
        "`~` is the shorthand for home directory in the path",
        "`Ctrl-c` will terminate a running command, so if one is taking a long time, use `ctrl-c` to kill it. If you want to copy something within the terminal, use `ctrl-shift-c` and `ctrl-shift-v`",
        "Many commands (man in particular) will give you a lot of information. Not all will be relevant. Don’t worry! Keep a cool head and just keep an eye out for useful stuff"
    ],
    1:[
        "Try using `man` on ls. The options that start with a `-` are called flags, they change the behavior of the command!"
    ],
    2:[
        "`cd` is case sensitive, make sure you spell the directory names correctly and use the right capitalization",
        "For directories that have a space in the name, you need to put the name in quotes or put a backslash (\\) before the space"
    ],
    3:[
        "You can type `/(search term)` to search for text within a man page"
    ],
    4:[
        "Investigate this folder with `ls -l`. Is there something weird about the sizes of the files? What commands can we use to find out more about the details of a particular… file ;).",
        "Try the optional example with the `cat` and `dog` files in the `ToLearn` directory to get a better handle on the `file` command."
    ],
    5:[
        "If you\'re having trouble creating an empty file, go over the definition of `touch` again",
        "Make sure your angle brackets are pointed the right way, and you have the right amount of them"
    ],
    6:[
        "Find is recursive! This means if you search one folder, it will search all folders in that one",
        "Don\'t worry if `find` gives you some `access denied` errors. Those are normal! If you\'d like to filter them out, try the trick in the angle brackets section"
    ],
    7:[
        "Find is recursive! This means if you search one folder, it will search all folders in that one",
        "The results you get from `find` will differ depending on where you run it",
        "There are many ways to use `find`, but most flags and arguments are optional and often unnecessary"
    ],
}


def main():
    ans = raw_input("Which question are you struggling with? If it\'s just in general, type 0. "
                "If you\'ve changed your mind, press enter without typing anything\n")
    if ans == '':
        return 0
    while (type(ans) == str and not ans.isdigit()) or int(ans) < 0 or int(ans) > 7:
        ans = raw_input("Invalid response! Please try again\n")
        if ans == '':
            return 0
    print(random.choice(hints[int(ans)]))
    print()
    ans = raw_input("Please rate your satisfaction with this hint! (`h` for helpful, `u` for unhelpful, `a` for already knew)."
                " If you wish to continue without providing feedback, press enter without typing anything.\n")
    while ans != 'h' and ans != 'u' and ans != 'a' and ans != '':
        ans = raw_input("Invalid input! Please respond with one of the listed options.\n")
    print("### Input Received ###")
    return 0


if __name__ == '__main__':
    main()
