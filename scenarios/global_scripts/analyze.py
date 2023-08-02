#!/usr/bin/python

#
# Copyright (C) 2018 University of Southern California.
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License,
# version 2, as published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#

# This code produces a CSV file for user interventions with the following columns
# CMBEGIN - fixed value
# node name
# epoch timestamp
# user home directory
# input command that the user has typed
# output, enclosed in % characters, could be multi-line
# username@node


import csv
import string
import sys
import os
import logging
import re
import codecs
import datetime
import time
import shutil
import queue
import subprocess
import threading


def starting_index_timestamp(line):
    """Return the index where the timestamp starts, in a line. If timestamp does not exist, return None"""
    reg_expr_end_timestamp = re.compile(';[0-9]+$')
    res = reg_expr_end_timestamp.search(line)
    if res is not None:
        return res.span()[0]
    else:
        return None

def get_ttylog_lines_from_file(ttylog, ttylog_seek_pointer):
    """Read from ttylog. If lines have '\r' at end, remove that '\r'. Return the read lines"""
    ttylog_file = open(ttylog,'r',errors='ignore', newline='\n')
    ttylog_file.seek(ttylog_seek_pointer)
    ttylog_read_data = ttylog_file.read()
    ttylog_file.close()
    ttylog_bytes_read = len(ttylog_read_data)
    ttylog_lines_file = []
    # If nothing new is there to read, return
    if ttylog_bytes_read == 0:
        return ttylog_lines_file, ttylog_bytes_read
    #Replace escaped double qoutes with qoutes
    ttylog_read_data = ttylog_read_data.replace(r'\"','"')
    ttylog_lines = ttylog_read_data.split('\n')

    for line in ttylog_lines:
        if len(line) > 0:
            if line[-1] == '\r':
                ttylog_lines_file.append(line[:-1])
            else:
                ttylog_lines_file.append(line)
        else:
            ttylog_lines_file.append(line)

    return ttylog_lines_file, ttylog_bytes_read


def decode(lines, current_user_prompt, current_root_prompt):

    if len(lines) == 0:
        return []

        #Reference for CSI: https://invisible-island.net/xterm/ctlseqs/ctlseqs.html

    escape_sequence_dict = {
    #Operating System Command. In xterm, they may also be terminated by BEL character. In xterm, the window title can be set by OSC 0;this is the window title BEL.
    #The sample line for root prompt is ']0;root@intro: ~root@intro:~# id;1554092145'
    'osc_reg_expr' : re.compile(r'\x1B][0-9]*;[\x20-\x7e]*\x07'),
    'csi_cursor_position' : re.compile(r'^[0-9]*;?[0-9]*H'),
    'csi_dec_private_mode_set' : re.compile(r'^\?(?:[0-9]*;?)*h'),
    'csi_dec_private_mode_reset' : re.compile(r'^\?(?:[0-9]*;?)*l'),
    'csi_character_attributes' : re.compile(r'^(?:[0-9]*;?)*m'),
    'csi_window_manipulation' : re.compile(r'^[0-9]*(?:;[0-9]*){2}t'),
    'csi_delete_n_chars' : re.compile(r'^\d*P'),
    'csi_tab' : re.compile(r'23@'),
    'csi_ctrlc' : re.compile(r'.*\^C.*'),
    'csi_cursor_up' : re.compile(r'^\d*A'),
    'controls_c1_esc_single_char' : re.compile(r'^[6789=>Fclmno|}~]')
    }
    buf = []
    i_line = 0
    decode_line_timestamp = ''
    current_user_prompt = ''
    current_root_prompt = ''

    for count, line in enumerate(lines):
        i_stream_line = 0
        cursor_pointer = 0  #points to the current position of cursor
        length_before_carriage_return = -1
        encountered_carriage_return = False
        buf.append([])

        p = re.compile(r'^User prompt is ')
        if p.match(line):
            current_user_prompt = line.split()[-1]
            node_name = line.split('@')[-1]
            current_root_prompt = 'root@' + node_name
            current_user_prompt = current_user_prompt.casefold()
            current_root_prompt = current_root_prompt.casefold()
            buf[i_line] = line
            i_line += 1
            continue

        #Eliminiating OSC for root prompt
        if escape_sequence_dict['osc_reg_expr'].findall(line):
            line = escape_sequence_dict['osc_reg_expr'].sub('',line)

        #If user prompt or root prompt does not occur at start of prompt, find the position of prompt. Now, The current line will end just before this prompt. A new line is constructed starting from the prompt.
        if (line.casefold().find(current_user_prompt) > 0) or (line.casefold().find(current_root_prompt) > 0):
            if (line.casefold().find(current_user_prompt) > 0):
                line_prompt_index = line.casefold().find(current_user_prompt)
            elif (line.casefold().find(current_root_prompt) > 0):
                line_prompt_index = line.casefold().find(current_root_prompt)
            next_line = line[line_prompt_index:]
            line = line[:line_prompt_index]
            lines.insert(count+1, next_line)

        timestamp_index = starting_index_timestamp(line)
        if timestamp_index is not None:
            decode_line_timestamp = line[timestamp_index:]
            line = line[:timestamp_index]

        # If the line consist of user prompt, but no timestamp
        if (len(current_user_prompt) > 0 or len(current_root_prompt) > 0) and ((line.casefold().find(current_user_prompt) == 0) or (line.casefold().find(current_root_prompt) == 0)) and timestamp_index is None and (count < len(lines) - 1):
            # Check if maybe we opened a text editor
            command_line_editors = ['vim', 'vi', 'nano', 'pico', 'emacs']
            Found = False
            for command_line_editor in command_line_editors:
                editor_position = line.find(command_line_editor)
                if (editor_position >  -1):
                    Found = True
            if not Found:
                start_ind = count + 1
                while start_ind < len(lines):
                    next_timestamp_index = starting_index_timestamp(lines[start_ind])
                    next_line = lines[start_ind]
                    if next_timestamp_index is not None:

                        decode_line_timestamp = next_line[next_timestamp_index:]
                        next_line = next_line[:next_timestamp_index]
                        line = line + next_line
                        lines.pop(start_ind)
                        break
                    else:
                        line = line + next_line
                        lines.pop(start_ind)

        len_line = len(line)
        while i_stream_line < len_line:
            #Skip the bell (^G) characters
            if line[i_stream_line] == '\x07':
                i_stream_line += 1

            #Carriage return ('\r') means to move the cursor at the start of the line
            # Carriage return also occurs in case of a 'soft wrap'
            elif line[i_stream_line] == '\r':
                #buf[i_line] = buf[i_line][:i_stream_line] + buf[i_line][i_stream_line + 1:]
                i_stream_line += 1
                encountered_carriage_return = True

            elif line[i_stream_line] == '\x08':
                if cursor_pointer > 0:
                    cursor_pointer -= 1
                i_stream_line += 1

            elif line[i_stream_line] == '\x1b' and line[i_stream_line + 1] == '[':
                i_stream_line += 2

                if i_stream_line >= len_line:
                    break

                if line[i_stream_line] == 'K' or (line[i_stream_line] in string.digits and line[i_stream_line + 1] == 'K'):
                    #If just K, then Erase from cursor to end of line. Else if 1K, erase from start of line to cursor. Else if 2K, erase whole line
                    n = int(line[i_stream_line]) if line[i_stream_line] in string.digits else 0
                    if n == 0:
                        buf[i_line] = buf[i_line][:cursor_pointer]
                    elif n == 1:
                        buf[i_line] = buf[i_line][cursor_pointer:]
                        cursor_pointer = 0
                    elif n == 2:
                        buf[i_line].clear()
                        cursor_pointer = 0
                    i_stream_line += 2 if line[i_stream_line] in string.digits else 1

                elif (line[i_stream_line] == '@') or (line[i_stream_line] in string.digits and line[i_stream_line + 1] == '@'):
                    """ make room for n characters at cursor """
                    n = int(line[i_stream_line]) if line[i_stream_line] in string.digits else 1
                    i_stream_line += 2 if line[i_stream_line] in string.digits else 1

                    # If carriage return was encountered
                    if encountered_carriage_return is True:
                        # Check if user prompt occurs immediately after
                        remaining_line = line[i_stream_line:]
                        if (remaining_line.find(current_user_prompt) == 0) or (remaining_line.find(current_root_prompt) == 0):
                            cursor_pointer = 0
                        elif cursor_pointer > 0:
                            # We do not decrease the cursor pointer if we are inserting characters (cursor_pointer -= 1)
                            length_before_carriage_return = cursor_pointer

                        encountered_carriage_return = False

                    #Read n characters
                    i = 0
                    while i < n and i_stream_line < len_line and cursor_pointer < i_stream_line:
                        buf[i_line].insert(cursor_pointer, line[i_stream_line])
                        cursor_pointer += 1
                        i_stream_line += 1
                        i += 1

                elif (line[i_stream_line] == 'C') or (line[i_stream_line] in string.digits and line[i_stream_line + 1] == 'C'):

                    """ move the cursor forward n columns """
                    n = int(line[i_stream_line]) if line[i_stream_line] in string.digits else 1
                    cursor_pointer += n
                    i_stream_line += 2 if line[i_stream_line] in string.digits else 1

                #If sequence is <0x1b>[J, <0x1b>[2J, <0x1b>[3J,  or <0x1b>[3;J, erase in display. Erasing from the start of the line, to the current cursor position
                elif line[i_stream_line] == 'J' or (line[i_stream_line] in string.digits and ( (line[i_stream_line + 1] == ';' and line[i_stream_line + 2] == 'J') or (line[i_stream_line + 1] == 'J') )):
                    cursor_pointer = 0
                    buf[i_line].clear()
                    if line[i_stream_line] == 'J':
                        i_stream_line += 1
                    elif line[i_stream_line] in string.digits:
                        if line[i_stream_line + 1] == ';' and line[i_stream_line + 2] == 'J':
                            i_stream_line += 3
                        elif line[i_stream_line + 1] == 'J':
                            i_stream_line += 2

                #Delete n characters. Sample is <0x1b>[17P (Delete 17 characters)
                elif escape_sequence_dict['csi_delete_n_chars'].match(line[i_stream_line:]):
                    move_cursor_control_characters = escape_sequence_dict['csi_delete_n_chars'].match(line[i_stream_line:]).span()[1]
                    n = -1
                    #If the pattern is <0x1b>[23P
                    if move_cursor_control_characters > 1:
                        n = int(line[i_stream_line: (i_stream_line + move_cursor_control_characters - 1) ] )
                    #If the pattern is <0x1b>[P
                    elif move_cursor_control_characters == 1:
                        n = 1
                    if n >=1 :
                        buf[i_line] = buf[i_line][:cursor_pointer] + buf[i_line][cursor_pointer + n:]
                        i_stream_line += move_cursor_control_characters

                #Delete tab character
                elif escape_sequence_dict['csi_tab'].match(line[i_stream_line:]):
                    i_stream_line += 3
                # Move cursor up 'n' lines. This is for moving cursor up.
                elif escape_sequence_dict['csi_cursor_up'].match(line[i_stream_line:]):
                    move_cursor_control_characters = escape_sequence_dict['csi_cursor_up'].match(line[i_stream_line:]).span()[1]
                    i_stream_line += move_cursor_control_characters

                    if length_before_carriage_return > -1:
                        cursor_pointer = cursor_pointer - length_before_carriage_return
                        if (cursor_pointer < 0):
                            cursor_pointer = 0

                #If sequence is <0x1b>[n;mH, escape it. This is for moving the cursor. <0x1b>[H movies the cursor to first row and column
                elif escape_sequence_dict['csi_cursor_position'].match(line[i_stream_line:]):
                    move_cursor_control_characters = escape_sequence_dict['csi_cursor_position'].match(line[i_stream_line:]).span()[1]
                    i_stream_line += move_cursor_control_characters

                #Skip the characters for character attributes. Samples are <0x1b>[7m and <0x1b>[27m
                elif escape_sequence_dict['csi_character_attributes'].match(line[i_stream_line:]):
                    move_cursor_control_characters = escape_sequence_dict['csi_character_attributes'].match(line[i_stream_line:]).span()[1]
                    i_stream_line += move_cursor_control_characters

                #Skip the characters for window manipulation. Samples are <0x1b>[20;0;0t
                elif escape_sequence_dict['csi_window_manipulation'].match(line[i_stream_line:]):
                    move_cursor_control_characters = escape_sequence_dict['csi_window_manipulation'].match(line[i_stream_line:]).span()[1]
                    i_stream_line += move_cursor_control_characters

                #Skip the characters for DEC Private Mode SET. Samples are <0x1b>[?5;7h
                elif escape_sequence_dict['csi_dec_private_mode_set'].match(line[i_stream_line:]):
                    move_cursor_control_characters = escape_sequence_dict['csi_dec_private_mode_set'].match(line[i_stream_line:]).span()[1]
                    i_stream_line += move_cursor_control_characters

                #Skip the characters for DEC Private Mode RESET. Samples are <0x1b>[?1024l
                elif escape_sequence_dict['csi_dec_private_mode_reset'].match(line[i_stream_line:]):
                    move_cursor_control_characters = escape_sequence_dict['csi_dec_private_mode_reset'].match(line[i_stream_line:]).span()[1]
                    i_stream_line += move_cursor_control_characters

            #Skip the C1 controls begining with Escape. Samples are <0x1b>>
            elif line[i_stream_line] == '\x1b' and escape_sequence_dict['controls_c1_esc_single_char'].match(line[(i_stream_line + 1):]):
                i_stream_line += 2

            #If it is a normal character
            else:
                # If carriage return was encountered
                if encountered_carriage_return is True:
                    # Check if user prompt occurs immediately after
                    remaining_line = line[i_stream_line:]
                    if (remaining_line.find(current_user_prompt) == 0) or (remaining_line.find(current_root_prompt) == 0):
                        cursor_pointer = 0
                    elif cursor_pointer > 0:
                        cursor_pointer -= 1
                        length_before_carriage_return = cursor_pointer

                    encountered_carriage_return = False

                if 0 <= cursor_pointer < len(buf[i_line]):
                    #Replace the character at cursor_pointer
                    buf[i_line][cursor_pointer] = line[i_stream_line]
                    cursor_pointer += 1

                elif cursor_pointer == len(buf[i_line]):
                    #Append the character
                    buf[i_line].append(line[i_stream_line])
                    cursor_pointer += 1

                i_stream_line += 1

        buf[i_line] = ''.join(buf[i_line])
        buf[i_line] += decode_line_timestamp
        decode_line_timestamp = ''

        i_line += 1

    return buf


def get_ttylog_lines_to_decode(ttylog_lines_read_next, ttylog_lines_from_file, known_prompts, current_root_prompt):
    # Return two lists
    # The first list contains the ttylog lines that should be read in next iteration of infinite loop.
    # The second list contain the ttylog lines that should be docded in current iteration of infinite loop.

    if len(ttylog_lines_from_file) == 0:
        return [], ttylog_lines_read_next

    elif len(ttylog_lines_from_file) >= 1:
        if len(ttylog_lines_read_next) > 0:
            ttylog_lines_read_next[-1] += ttylog_lines_from_file[0]
            if len(ttylog_lines_from_file) > 1:
                ttylog_lines_read_next.extend(ttylog_lines_from_file[1:])
        else:
            ttylog_lines_read_next.extend(ttylog_lines_from_file)

    index_ttylog_lines_file = None
    line_prompt_end_index = -1
    line_to_append = ''
    current_root_prompt = current_root_prompt.casefold()

    # When we get two user prompts in ttylog_lines_read_next, we add all the lines from first user prompt to second user prompt to ttylog_lines_to_decode.
    # Second user prompt line is not inclusive
    no_of_prompts_in_ttylog_read_next = 0

    # Make a Reverse copy of the ttylog_lines_from_file list
    ttylog_next_reverse = ttylog_lines_read_next[::-1]
    for count, line in enumerate(ttylog_next_reverse):
        if r'END tty_sid' in line:
            ttylog_lines_to_decode = ttylog_lines_read_next[::]
            ttylog_lines_read_next = []
            return ttylog_lines_to_decode, ttylog_lines_read_next
        elif any(p.casefold() in line.casefold() for p in known_prompts):
            no_of_prompts_in_ttylog_read_next += 1
            # Break the loop of no_of_prompts >= 2
            if no_of_prompts_in_ttylog_read_next >= 2:
                break

            # Get index of this line in ttylog_lines_file
            index_ttylog_lines_file = len(ttylog_lines_read_next) - 1 - count

            # Find the last user prompt. Get data starting from 0th index to ending of last user prompt from the line
            for p in known_prompts:
                if (line.casefold().rfind(p) > -1):
                    line_prompt_end_index = line.casefold().rfind(p)
                    line_prompt_end_index = line_prompt_end_index + len(p)
                    break
            line_to_append = line[:line_prompt_end_index]

    if index_ttylog_lines_file is not None and no_of_prompts_in_ttylog_read_next >= 2:

        ttylog_lines_to_decode = ttylog_lines_read_next[:index_ttylog_lines_file]

        # Add the line containing user/root prompt to ttylog_lines_to_decode so that the most recently executed command can be parsed.
        # The characters from 0th index till ending of last user prompt is included is contained in line_to_append
        if len(line_to_append) > 0:
            ttylog_lines_to_decode.append(line_to_append)

        ttylog_lines_read_next = ttylog_lines_read_next[index_ttylog_lines_file:]
        return ttylog_lines_to_decode, ttylog_lines_read_next

    else:
        return [], ttylog_lines_read_next


def push_files_github_user_dir(input_command, line_timestamp, local_copy_directory, files_path_list, user_home_dir, current_line_prompt, node_name, global_copy_directory, max_allowed_file_size = 5*(2**20)):
    """Push files to github user repo"""
    if (len(files_path_list) == 0) or not (os.path.isdir(local_copy_directory)):
        return

    if (len(local_copy_directory) > 0) and (local_copy_directory[-1] != r'/'):
        local_copy_directory += r'/'

    copy_directory = local_copy_directory

    for file_path in files_path_list:

        # If the file does not exist OR file size > max allowed file size, then continue
        if (not os.path.isfile(file_path)) or (os.path.getsize(file_path) > max_allowed_file_size):
            continue

        # Normalize the pathname
        # os.path.abspath('/var/../done/') will return '/done'
        file_path = os.path.abspath(file_path)

        file_dir, file_name = os.path.split(file_path)
        if file_dir.find(user_home_dir) == 0:
            len_user_home_dir = len(user_home_dir)
            file_dir = file_dir[len_user_home_dir:]
            copy_directory = global_copy_directory

        # Remove the '/' from file_dir, since github_user_directory has a '/' at its end
        if (len(file_dir) > 0) and (file_dir[0] == r'/'):
            file_dir = file_dir[1:]

        # Add a '/' at the ending of file_dir
        if (len(file_dir) > 0) and (file_dir[-1] != '/'):
            file_dir = file_dir + "/"

        file_copy_destination_dir = copy_directory + file_dir

        # Create the directory if it does not exist
        if not os.path.isdir(file_copy_destination_dir):
            os.makedirs(file_copy_destination_dir)

        file_copy_destination = file_copy_destination_dir + file_name
        # Copy the file to destination
        try:
            shutil.copy2(file_path, file_copy_destination)
        except PermissionError as e:
            continue

    # Get github user directory from copy_directory
    # github_user_directory will be the parent of the parent directory
    # If local_copy_directory = '/tmp/upload_modified_files/exp-1/node_a/'
    # os.path.dirname(os.path.dirname(local_copy_directory[:-1])) will return '/tmp/upload_modified_files'
    github_user_directory = os.path.dirname(os.path.dirname(local_copy_directory[:-1])) + r'/'

    # Get username from user prompt
    user_name = current_line_prompt.split('@')[0]

    # Add all files in copy_directory to staging area
    subprocess.run(['git','-C', github_user_directory, 'add', copy_directory])
    # Commit the changes
    subprocess.run(['git', '-C', github_user_directory, 'commit', '-m', "Adding files by {} at {} with command {} on node {}".format(user_name, line_timestamp, input_command, node_name)], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    # Rebasing to get all commits from origin, and to put our commits on top of the comits received by origin
    #subprocess.run(['git', '-C', github_user_directory, 'pull', '--rebase', '-X', 'theirs'], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    subprocess.run(['git', '-C', github_user_directory, 'pull'], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
    # Push the changes
    subprocess.run(['git', '-C', github_user_directory, 'push'], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

    return True


def get_github_user_directory(github_repo_name='upload_modified_files', local_dir_to_clone_github='/tmp/'):
    """Return the github user directory where the files will be copied"""

    # Get the project name and experiment name
    with open(r'/var/emulab/boot/nickname','r') as file_handle:
        file_data = file_handle.read().splitlines()[0]
    node, exp_name, proj_name = file_data.split('.')

    github_base_directory = '/proj/{}/{}/'.format(proj_name, github_repo_name)


    # Return if the github repo does not exist
    if not os.path.isdir(github_base_directory):
        return None

    # Add a '/' at the ending of file_dir
    if local_dir_to_clone_github[-1] != '/':
        local_dir_to_clone_github = local_dir_to_clone_github + "/"

    # Clone the github repo
    subprocess.run(['git','-C', local_dir_to_clone_github, 'clone', github_base_directory], stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

    # Construct directory where users file will be copied
    local_copy_directory = local_dir_to_clone_github + github_repo_name + r'/' + exp_name + r'/' + node + r'/'
    global_copy_directory = local_dir_to_clone_github + github_repo_name + r'/' + exp_name + r'/'

    # Create the github user directory does not exist, if it does not exist
    if not os.path.isdir(local_copy_directory):
        os.makedirs(local_copy_directory)

    return local_copy_directory, global_copy_directory


def get_filenames_from_user_command(current_working_directory, input_command, user_prompt, user_home_dir):
    """If input_command contains file(s), return a list of absolute paths of file(s)"""

    if current_working_directory[-1] != r'/':
        current_working_directory += r'/'

    # Make the input command lower case and remove whitespaces from start and end of string
    input_command = input_command.strip()
    list_of_filenames = []
    absolute_filesnames = []

    # Check for output redirection
    if (r'>' in input_command) or (r'>>' in input_command):
        file_name = ''
        # Assumption: Only one of '>' or '>>' is present in input_command
        if (r'>>' not in input_command) and (r'>' in input_command):
            file_name = input_command.split('>',maxsplit=1)[1].strip()
        elif r'>>' in input_command:
            file_name = input_command.split('>>',maxsplit=1)[1].strip()

        list_of_filenames.append(file_name)

    # Check if a command line editor was used to access file
    else:
        command_line_editors = ['vim ', 'vi ', 'nano ', 'pico ', 'emacs ']
        for command_line_editor in command_line_editors:
            editor_position = input_command.find(command_line_editor)
            # If the input command contains an editor

            if editor_position > -1:
                #logfile = open(r"/tmp/acont.log", "a")
                #logfile.write("Found editor in line "+input_command+"\n")
                #logfile.close()

                input_command = input_command[editor_position:]

                # Get a new command without the editor's name
                new_command = input_command.split(' ',maxsplit=1)[1]

                # If the filename is 'test file', and user enters it as 'vim "test file"'
                temp_names = re.findall(r'"[A-Za-z0-9_/#.~]+\s[A-Za-z0-9_/#.~]+"', new_command)
                list_of_filenames.extend(temp_names)
                new_command = re.sub(r'"[A-Za-z0-9_/#.~]+\s[A-Za-z0-9_/#.~]+"', '', new_command).strip()

                # If the filename contains spaces, and its interpreded as 'vim a\ b'
                temp_names = re.findall(r'[A-Za-z0-9_/#.~]+\\\s[A-Za-z0-9_/#.~]+', new_command)
                list_of_filenames.extend(temp_names)
                new_command = re.sub(r'[A-Za-z0-9_/#.~]+\\\s[A-Za-z0-9_/#.~]+', '', new_command).strip()

                # Get arguments list in command. Skip the first argument, since it would be the editor's name
                arguments_list_in_command = new_command.split()
                for argument_name in arguments_list_in_command:
                    # If the argument is not a command line option
                    if (r'--' != argument_name[:2]) and (r'-' != argument_name[:1]):
                        list_of_filenames.append(argument_name)
                        #logfile = open(r"/tmp/acont.log", "a")
                        #logfile.write("Argument name "+argument_name+"\n")
                        #logfile.close()
                break


    for file_name in list_of_filenames:

        # If the filename contains spaces,such as 'a\ b', make it 'a b'
        file_name = file_name.replace('\ ',' ')
        # Strip for whitespaces, single qoutes, and double quotes
        file_name = file_name.strip(" ")
        file_name = file_name.strip('"')
        file_name = file_name.strip("'")

        final_file_name = ''
        if file_name[0] == r'/':
            final_file_name = file_name
        elif file_name[0] == r'~':
            user_name = user_prompt.split('@')[0]
            if user_name == 'root':
                final_file_name = r'/root' + file_name
            else:
                final_file_name = file_name.replace('~', user_home_dir ,1)
        else:
            final_file_name = current_working_directory + file_name
        absolute_filesnames.append(final_file_name)
        #logfile = open(r"/tmp/acont.log", "a")
        #logfile.write("Appended "+final_file_name+"\n")
        #logfile.close()

    return absolute_filesnames


def process_files_from_queue():
    """Process the elements in queue """
    global files_list_queue
    while True:

        # Get element from queue in a blocking call
        try:
            queue_element = files_list_queue.get(True, 0.1)
        except queue.Empty as e:
            #print("Got nothing")
            time.sleep(1)
            continue

        line_command = queue_element[0]
        line_timestamp = queue_element[1]
        github_local_user_directory = queue_element[2]
        github_files_path_list = queue_element[3]
        current_home_dir = queue_element[4]
        current_line_prompt = queue_element[5]
        node_name = queue_element[6]
        push_files_github_user_dir(line_command, line_timestamp, github_local_user_directory, github_files_path_list, current_home_dir, current_line_prompt, node_name, github_global_user_directory)

        files_list_queue.task_done()


def write_to_csv(line):

    csvfile = open(csv_output_file,'a', newline='')
    csvwriter = csv.writer(csvfile, delimiter=',', quotechar='%', quoting=csv.QUOTE_MINIMAL)
    csvwriter.writerow([line['id'],line['node_name'],line['timestamp'],line['cwd'], line['cmd'], line['output'], line['prompt']])
    csvfile.close()

def get_unique_id_dict():
    """Return a dictonary containing information about the unique ID that will be inserted in every row in output CSV"""
    unique_id_dict = {
        'counter':-1,
        'start_time':round(datetime.datetime.now().timestamp())
    }

    # Get the experiment name
    try:
        with open(r'/var/emulab/boot/nickname','r') as file_handle:
            file_data = file_handle.read().splitlines()[0]
            node, exp_name, proj_name = file_data.split('.')
    except (FileNotFoundError, PermissionError) as e:
        exp_name = 'edulog'
    finally:
        unique_id_dict['exp_name'] = exp_name

    return unique_id_dict


if __name__ == "__main__":

    global line_timestamp
    global line_command
    global output_prevous_command
    global node_name

    global current_line_prompt
    global current_home_dir
    global current_working_directory
    global current_session_id
    global is_current_prompt_root
    global unique_id_dict
    global unique_row_id
    global ttylog_sessions
    global output_prevous_command
    global root_prompt
    global root_home_dir
    global github_local_user_directory
    global github_files_path_list
    global exit_flag
    global files_list_queue

    #The input ttylog file path is stored in 'ttylog'
    ttylog = sys.argv[1]
    #The output CSV file path is stored in 'csv_output_file'
    csv_output_file = sys.argv[2]
        # if not os.path.isfile(ttylog):
        #     logging.critical("there's a problem with ttylog! aborting.")
        #     exit(1)

    # Get the unique id dictionary.
    # This dictionary will be used to uniquely identif a row in CSV file
    unique_id_dict = get_unique_id_dict()

    ttylog_sessions = {}
    output_prevous_command = ''
    current_session_id = ''
    first_ttylog_line = True
    input_cmd = ''
    output_txt = ''
    root_home_dir = '/root'
    node_name = ''
    is_current_prompt_root = False
    ttylog_seek_pointer = 0
    user_initial_prompt = ''
    root_prompt = ''
    skip_reading_in_first_iteration = True
    ttylog_lines_read_next = []
    exit_flag = False
    known_prompts = []
    host_pattern = ''

    ttylog_lines_from_file, ttylog_bytes_read = get_ttylog_lines_from_file(ttylog, ttylog_seek_pointer)
    ttylog_seek_pointer += ttylog_bytes_read


    for count, line in enumerate(ttylog_lines_from_file):

        #Get the tty_sid from first line of the session
        if r'starting session w tty_sid' in line:
            index_start = line.find(r'starting session w tty_sid')
            if index_start == 0:
                p = re.compile(r'starting session w tty_sid:\d+$')
                if p.match(line):
                    session_id = line.split()[-1]
                    # Check if already exists
                    if session_id in ttylog_sessions.keys():
                        continue
                    ttylog_sessions[session_id] = {}
                    ttylog_sessions[session_id]['lines'] = []
                    current_session_id = session_id
                    continue
            #If there is a case, 'test@client:~$ starting session w tty_sid:18', move 'starting session w tty_sid:18' to next line. This is done to get the details of the last executed command. A row in csv is written, when a prompt is encountered.
            elif index_start > 0:
                next_line = line[index_start:]
                line = line[:index_start]
                ttylog_lines.insert(count + 1, next_line)

        #Get the user prompt from the second line of the session
        #Same line is 'User prompt is test@intro')
        p = re.compile(r'^User prompt is ')
        if p.match(line):
            user_initial_prompt = (line.split()[-1])
            ttylog_sessions[current_session_id]['initial_prompt'] = user_initial_prompt
            node_name = line.split('@')[-1]
            root_prompt = 'root@' + node_name
            is_current_prompt_root = False
            continue

        #Get the user home directory from third line of the session
        if r'Home directory is' in line:
            home_directory = line.split()[-1]
            ttylog_sessions[current_session_id]['home_dir'] = home_directory
            first_ttylog_line = True
            break_counter = count + 1
            ttylog_lines_from_file = ttylog_lines_from_file[break_counter:]
            break

    # populate the list of known_prompts, and construct a regex pattern for possible hosts
    nodes = []
    try:
        file = open('/usr/local/src/ttylog/host_names', 'r')
        nodes = file.read().splitlines()
        file.close()
        host_pattern = '(' + '|'.join(n for n in nodes) + ')'
        for node in nodes:
            known_prompts.append(user_initial_prompt.split('@')[0] + '@' + node)
    except FileNotFoundError:
        print('File /usr/local/src/ttylog/host_names.txt not found', file=sys.stderr)
        known_prompts.append(user_initial_prompt)

    while True:

        # Skip reading of ttylog in first iteration of loop. The program already read ttylog file outside of loop
        if not skip_reading_in_first_iteration:
            ttylog_lines_from_file, ttylog_bytes_read = get_ttylog_lines_from_file(ttylog, ttylog_seek_pointer)
            ttylog_seek_pointer += ttylog_bytes_read

        if skip_reading_in_first_iteration == True:
            skip_reading_in_first_iteration = False

        ttylog_lines_to_decode, ttylog_lines_read_next = get_ttylog_lines_to_decode(ttylog_lines_read_next, ttylog_lines_from_file, known_prompts, root_prompt)
        if len(ttylog_lines_to_decode) == 0:
            time.sleep(0.1)
            continue

        ttylog_lines = decode(ttylog_lines_to_decode, user_initial_prompt, root_prompt)

        for count,line in enumerate(ttylog_lines):
            # Check for ctrl c and remove
            #print("Line ", line)
            rexp = re.compile('.*\^C')
            m = rexp.search(line)
            if m is not None:
                tline = rexp.sub('', line)
                line = tline

            command_pattern_user_prompt = re.compile("{user}@{host}:.*?".format(user=user_initial_prompt.split('@')[0].casefold(), host=host_pattern))
            command_pattern_root_prompt = re.compile("{}:.*?".format(root_prompt.casefold()))
            tstampre = re.compile(";\d{9}")
            # Check if there is a prompt
            res = command_pattern_user_prompt.search(line.casefold())
            if (res or command_pattern_root_prompt.search(line.casefold())):
                if (res):
                    user_prompt = res.group(0).split(':')[0]
                else:
                    user_prompt = root_prompt
                prompt = True
            else:
                prompt = False

            # Check if there is a timestamp
            tmatch = tstampre.search(line)
            if tmatch:
                haststamp = True
            else:
                haststamp = False

            # Check if there is end
            end = False
            if r'END tty_sid' in line:
                end = True

            #print("Line ", line, " prompt ", prompt, " input cmd ", input_cmd)
            if (prompt) or (not prompt and first_ttylog_line):
                isinput = True
                unique_row_id = "{}:{}:{}".format(unique_id_dict['exp_name'],unique_id_dict['start_time'],unique_id_dict['counter'])
                if prompt:
                    if command_pattern_root_prompt.search(line.casefold()):
                        left_hash_part, right_hash_part = line.split('#',1)
                        current_line_prompt = left_hash_part
                        node_name = left_hash_part.split('@')[-1].split(':')[0]
                        current_working_directory = left_hash_part.split(':',1)[-1]
                        current_working_directory = current_working_directory.replace('~', root_home_dir ,1)
                        line = right_hash_part[1:]
                    else:
                        left_dollar_part, right_dollar_part = line.split('$',1)
                        current_line_prompt = left_dollar_part
                        node_name = left_dollar_part.split('@')[-1].split(':')[0]
                        current_working_directory = left_dollar_part.split(':',1)[-1]
                        current_working_directory = current_working_directory.replace('~', ttylog_sessions[current_session_id]['home_dir'] ,1)
                        line = right_dollar_part[1:]
                else:
                    current_working_directory = home_directory
                    user_prompt = user_initial_prompt
                    current_line_prompt = user_prompt
            else:
                isinput = False

            line_timestamp = 0

            if haststamp:
                indexts = tstampre.search(line)
                line_timestamp = line[indexts.span()[0]+1:indexts.span()[1]+1]
                line = line[:indexts.span()[0]]


            my_timestamp = int(time.time())

            if isinput:
                input_cmd = line
                unique_id_dict['counter'] +=1
                unique_row_id = "{}:{}:{}".format(unique_id_dict['exp_name'],unique_id_dict['start_time'],unique_id_dict['counter'])
                # Save previous output
                if not first_ttylog_line:
                    if len(output_txt) > 500:
                        output_txt = output_txt[:500]

                    unique_row_pid = "{}:{}:{}".format(unique_id_dict['exp_name'],unique_id_dict['start_time'],unique_id_dict['counter']-1)
                    cline = len(ttylog_sessions[current_session_id]['lines']) - 1
                    if cline >=0:
                        #print("Cline ", cline, " output ", output_txt, " prompt ", ttylog_sessions[current_session_id]['lines'][cline]['prompt'])
                        ttylog_sessions[current_session_id]['lines'][cline]['output'] = output_txt
                        write_to_csv(ttylog_sessions[current_session_id]['lines'][cline])
                        #logfile = open(r"/tmp/acont.log", "a")
                        #logfile.write("Logged input "+ttylog_sessions[current_session_id]['lines'][cline]['cmd']+"\n")
                        #logfile.write("Logged output "+ttylog_sessions[current_session_id]['lines'][cline]['output']+"\n")
                        #logfile.close()
                # Save current input and save into github if needed
                new_line = dict()
                new_line['id'] = unique_row_id
                new_line['timestamp'] = my_timestamp
                new_line['output'] = ""
                new_line['node_name'] = node_name
                new_line['cwd'] = current_working_directory
                new_line['cmd'] = input_cmd
                new_line['prompt'] = current_line_prompt
                ttylog_sessions[current_session_id]['lines'].append(new_line)
                #logfile = open(r"/tmp/acont.log", "a")
                #logfile.write("Found input "+input_cmd+"\n")
                #logfile.close()
                current_home_dir = ttylog_sessions[current_session_id]['home_dir']
                output_txt = ''

            elif not end:
                output_txt += '\n'+line
            else:
                # End, save what we can
                if len(output_txt) > 500:
                    output_txt = output_txt[:500]
                unique_row_pid = "{}:{}:{}".format(unique_id_dict['exp_name'],unique_id_dict['start_time'],unique_id_dict['counter']-1)
                cline = len(ttylog_sessions[current_session_id]['lines']) - 1
                if cline >=0:
                    ttylog_sessions[current_session_id]['lines'][cline]['output'] = output_txt
                    write_to_csv(ttylog_sessions[current_session_id]['lines'][cline])
                    #logfile = open(r"/tmp/acont.log", "a")
                    #logfile.write("Logged input "+ttylog_sessions[current_session_id]['lines'][cline]['cmd']+"\n")
                    #logfile.write("Logged output "+ttylog_sessions[current_session_id]['lines'][cline]['output']+"\n")
                    #logfile.close()
            first_ttylog_line = False

        time.sleep(0.1)

        if exit_flag:
            exit(0)
