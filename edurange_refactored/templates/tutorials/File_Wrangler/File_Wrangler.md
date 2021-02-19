# File Wrangler

---

## Learning Objectives
1. Become familiar with ls and common flags: -a, -l
2. (see [Getting Started](https://github.com/edurange/edurange-flask/blob/master/edurange_refactored/templates/tutorials/Getting_Started/Getting_Started.md
)) Know how to search man pages to find a specific option.
3. Navigate file system to find specific files
4. Move and copy files.
5. Set permissions (access control) for files.

## Task 1

The `pwd` command will give you the current working directory. This tells you where you are in the Linux file system.

Steps:

1. Type `pwd` into the prompt

2. Answer question 1 in EDURange.

---

## Task 2

The `man` command outputs the manual entry for a given command. The format is as follows:

`man [command]`

Steps:

1. View the manual entry for the `pwd` command by replacing with `pwd`. (Note that you need to type `q` to get out of the manual!)

2. Answer question 2 in EDURange.

---

## Task 3

Now that we know where we are, we will want to know what is in this directory. For a simple list of files and directories, you would use the list command.

Steps:

1. Type `ls` into the prompt for a list of files and directories.

2. Answer question 3 in EDURange.

---

## Task 4

Steps:

1. View the manual entry for the `ls` command. Notice in the `SYNOPSIS`, the format of the command is as follows:

`ls [OPTION]... [FILE]...`

Anything in square brackets is optional. In this case, we can use `ls` along with one of the options listed with `-` or `--` and we could add a complete file path.

2. Scroll through to manual to find the option that will provide a long listing format for the `ls` command.

3. Answer question 4 in EDURange.

4. Try this command with the option you found. Don’t forget to include the `-` or `--`! You can immediately tell whether the item is a file or a directory by the very first character provided in the output. Files are denoted by a `-` and directories are denoted by a `d`.

5. Answer question 5 in EDURange.

---

## Task 5

The `cd` command allows you to change into another directory. The format is as follows:

`cd`

Steps:

1. Change into the view directory and run the list (`ls`) command to view the files in this directory.

2. Answer question 6 in EDURange.

---

## Task 6

Hidden files begin with a `'.'` and are not displayed unless you specify an option with the `ls` command.

Steps:

1. View the manual entry for the `ls` command again.

2. Scroll through to manual to find the option that will not ignore files that start with a `'.'`.

3. Answer question 7 in EDURange.

4. Try this command with the option you found. You should see any hidden files or folders (those beginning with a `'.'`).

5. Answer question 8 in EDURange.

---

## Task 7

To go back a directory, you would type the following command:

`cd ..`

The command `pwd`, will show you where you are in the Linux file system.

Steps:

1. Type `cd ..` into the prompt.

2. Type `pwd` into the prompt. You should see that you are back in the home directory for the account you log in with.

3. Answer question 9 in EDURange.

---

## Task 8

You can chain options for a single command. So, for example, you could include both the options for long listing and listing hidden files by simply adding each option after the `ls` command.

Steps:

1. Type this chained command now. You should now see all files and folders, including those that are hidden, and all of the details about them.

2. Answer question 10 in EDURange.

---

## Task 9

Steps:

1. Change into the manipulate directory and run the list (`ls`) command to view the files in this directory.

2. Renaming files

	- a. Look up the manual entry for the `mv` command

	- b. Use the `mv` command to rename `file1.txt` to `renamed_file1.txt`. Be sure to be exact!

3. Copying files

	- a. Look up the manual entry for the `cp` command.

	- b. Use the `cp` command to copy `file2.txt` to `copied_file2.txt`.

4. Type the following into the prompt for the flag: `sudo manflag`

5. Answer question 11 in EDURange.

6. Go back to your home directory, and then go to the permissions directory.

---

## Task 10

Steps:

1. run the list (`ls`) command to view the files in this directory.

2. Read the following resource on Linux file permissions: http://linuxcommand.org/lc3_lts0090.php

3. Copy the `perm1.txt` to `copied_perm1.txt`.

4. Changing permissions

	- a. Look up the manual entry for the `chmod` command.

	- b. Use the `chmod` command to change the permissions of `copied_perm1.txt` to:

		- i. Owner = Read + Write

		- ii. Group = Read + Write

		- iii. User = No permissions

	- c. Copy the `perm2.txt` to `copied_perm2.txt`

	- d. Use the `chmod` command to change the permissions of `copied_perm2.txt` to:

		- i. Owner = Read + Write + Execute

		- ii. Group = Read + Write

		- iii. User = Read only

5. Type the following into the terminal for the flag: `sudo perflag`

6. Answer question 12 in EDURange.

Exercise Complete!

---
