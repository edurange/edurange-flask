#!/usr/bin/python

import csv
import string
import sys
import os.path
import logging
import re
import codecs
import datetime

def starting_index_timestamp(line):
    """Return the index where the timestamp starts, in a line. If timestamp does not exist, return None"""
    reg_expr_end_timestamp = re.compile(';[0-9]+$')
    res = reg_expr_end_timestamp.search(line)
    if res is not None:
        return res.span()[0]
    else:
        return None

def get_ttylog_lines_from_file(ttylog):
    """Read from ttylog. If lines have '\r' at end, remove that '\r'. Return the read lines"""
    ttylog_file = open(ttylog,'r',errors='ignore', newline='\n')
    ttylog_read_data = ttylog_file.read()
    ttylog_file.close()
    ttylog_lines = ttylog_read_data.split('\n')
    ttylog_lines_file = []

    for line in ttylog_lines:
        if len(line) > 0:
            if line[-1] == '\r':
                ttylog_lines_file.append(line[:-1])
            else:
                ttylog_lines_file.append(line)

    return ttylog_lines_file

def decode(lines):

    #Reference for CSI: https://invisible-island.net/xterm/ctlseqs/ctlseqs.html

    escape_sequence_dict = {
    #ESC] OSC – Operating System Command. In xterm, they may also be terminated by BEL character. In xterm, the window title can be set by OSC 0;this is the window title BEL.
    #The sample line for root prompt is ']0;root@intro: ~root@intro:~# id;1554092145'
    'osc_reg_expr' : re.compile(r'\x1B]0;.*\x07'),
    'csi_cursor_position' : re.compile(r'^[0-9]*;?[0-9]*H'),
    'csi_dec_private_mode_set' : re.compile(r'^\?(?:[0-9]*;?)*h'),
    'csi_dec_private_mode_reset' : re.compile(r'^\?(?:[0-9]*;?)*l'),
    'csi_character_attributes' : re.compile(r'^(?:[0-9]*;?)*m'),
    'csi_window_manipulation' : re.compile(r'^[0-9]*(?:;[0-9]*){2}t')
    }
    
    buf = []
    i_line = 0
    decode_line_timestamp = ''
    for count, line in enumerate(lines):
        i_stream_line = 0
        cursor_pointer = 0  #points to the current position of cursor
        buf.append([])

        #Eliminiating OSC for root prompt
        if escape_sequence_dict['osc_reg_expr'].findall(line):
            line = escape_sequence_dict['osc_reg_expr'].sub('',line)

        timestamp_index = starting_index_timestamp(line)
        if timestamp_index is not None:
            decode_line_timestamp = line[timestamp_index:]
            line = line[:timestamp_index]
        len_line = len(line)

        while i_stream_line < len_line:
            
            #Skip the bell (^G) characters
            if line[i_stream_line] == '\x07':
                i_stream_line += 1
            
            #Carriage return ('\r') means to move the cursor at the start of the line
            elif line[i_stream_line] == '\r':
                cursor_pointer = 0
                i_stream_line += 1

            elif line[i_stream_line] == '\x08':
                if cursor_pointer > 0:
                    cursor_pointer -= 1
                i_stream_line += 1

            elif line[i_stream_line] == '\x1b' and line[i_stream_line + 1] == '[':
                i_stream_line += 2

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
                    #Read n characters
                    i = 0
                    while i < n:
                        buf[i_line].insert(cursor_pointer, line[i_stream_line])
                        cursor_pointer += 1
                        i_stream_line += 1
                        i += 1
                    
                elif (line[i_stream_line] == 'C') or (line[i_stream_line] in string.digits and line[i_stream_line + 1] == 'C'):
                    """ move the cursor forward n columns """
                    n = int(line[i_stream_line]) if line[i_stream_line] in string.digits else 1
                    cursor_pointer += n
                    i_stream_line += 2 if line[i_stream_line] in string.digits else 1

                elif (line[i_stream_line] == 'P') or (line[i_stream_line] in string.digits and line[i_stream_line + 1] == 'P'):
                    """ delete n chars  """
                    n = int(line[i_stream_line]) if line[i_stream_line] in string.digits else 1
                    buf[i_line] = buf[i_line][:cursor_pointer] + buf[i_line][cursor_pointer + n:]
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

            #If it is a normal character
            else:
                if cursor_pointer < len(buf[i_line]):
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


def sort_ttylog_lines(line):
    return line[1]

if __name__ == "__main__":

    ttylog = sys.argv[1]
    csv_output_file = sys.argv[2]
        # if not os.path.isfile(ttylog):
        #     logging.critical("there's a problem with ttylog! aborting.")
        #     exit(1)

    ttylog_lines_file = get_ttylog_lines_from_file(ttylog)
    ttylog_lines = decode(ttylog_lines_file)
    ttylog_sessions = {}
    current_session_id = ''
    output_prevous_command = ''
    first_ttylog_line = 0
    root_home_dir = '/root'
    node_name = ''
    is_current_prompt_root = False

    for line in ttylog_lines:
        #Get the tty_sid from first line of the session
        if r'starting session w tty_sid' in line:
            session_id = line.split()[-1]
            ttylog_sessions[session_id] = {}
            current_session_id = session_id
            continue

        #Get the user prompt from the second line of the session
        #Same line is 'User prompt is test@intro'
        if r'User prompt is' in line:
            user_initial_prompt = line.split()[-1]
            ttylog_sessions[current_session_id]['initial_prompt'] = user_initial_prompt
            node_name = line.split('@')[-1]
            root_prompt = 'root@' + node_name
            is_current_prompt_root = False
            continue

        #Get the user home directory from third line of the session
        if r'Home directory is' in line:
            home_directory = line.split()[-1]
            ttylog_sessions[current_session_id]['home_dir'] = home_directory
            first_ttylog_line = 1
            continue

        copy_of_line = line
        #Get the first user entered command
        if first_ttylog_line:
            ttylog_sessions[current_session_id]['lines'] = []
            user_prompt = ttylog_sessions[current_session_id]['initial_prompt']
            #Sample first line without user prompt is 'ls;1553743080'
            #casefold method is used for case insensitive search. While displaying the node name, there was a case where bash displayed 'nOdeA' as 'nodea'
            if user_prompt.casefold() not in line.casefold():
                current_working_directory = ttylog_sessions[current_session_id]['home_dir']
            #Sample first line with user prompt is 'test@intro:~$ ls;1554089050'

            elif user_prompt.casefold() in line.casefold():
                #If user uses root user to SSH, then the first line is for root_prompt
                #Assumption: user_prompt = root_prompt, if user uses root to SSH
                if root_prompt.casefold() == user_prompt.casefold():
                    left_hash_part, right_hash_part = line.split('#',1)
                    current_working_directory = left_hash_part.split(':',1)[-1]
                    current_working_directory = current_working_directory.replace('~', root_home_dir ,1)
                    right_hash_part = right_hash_part[1:]
                else:
                    left_dollar_part, right_dollar_part = line.split('$',1)
                    current_working_directory = left_dollar_part.split(':',1)[-1]
                    current_working_directory = current_working_directory.replace('~', ttylog_sessions[current_session_id]['home_dir'] ,1)
                    line = right_dollar_part[1:]


            #Incase the user closes the terminal, without using the 'exit' command, line is like 'test@intro:~$'
            if len(line) == 0:
                continue

            line_split = line.split(';')

            if line_split[-1].isdigit():
                line_timestamp = int(line_split[-1])
                line_command = ';'.join(line_split[:-1] )
            else:
                line_timestamp = 0

            #line_timestamp = int(line_split[-1])
            #line_command = ';'.join(line_split[:-1] )
            first_ttylog_line = 0
            continue

        #Get the commands from lines
        #If user uses root to SSH, don't run the following 'elif' section
        elif ttylog_sessions[current_session_id]['initial_prompt'].casefold() in line.casefold() and ttylog_sessions[current_session_id]['initial_prompt'].casefold() != root_prompt.casefold(): 
            #If line is like 'googletest@intro:~$ ls;1554089474', 'google' is output of previous command
            start_of_prompt = line.casefold().find(user_prompt.casefold())
            if start_of_prompt > 0:
                output_till_start_of_prompt = line[:start_of_prompt]
                output_prevous_command += output_till_start_of_prompt + "\n"
                line = line[start_of_prompt:]
            
            if line_timestamp > 0 and len(line_command) > 0:
                #If earlier the prompt was root, and now the prompt is of normal user, append using root_prompt for this line. Afterwards, set 'is_current_prompt_root' to False, and append using 'user_prompt'
                if is_current_prompt_root == True:
                    ttylog_sessions[current_session_id]['lines'].append(['CMBEGIN', node_name, line_timestamp, current_working_directory, line_command, output_prevous_command, root_prompt])
                    is_current_prompt_root = False
                else:
                    ttylog_sessions[current_session_id]['lines'].append(['CMBEGIN', node_name, line_timestamp, current_working_directory, line_command, output_prevous_command, user_prompt])
                line_timestamp = 0
                line_command = ''
            
            output_prevous_command = ''

            #Sample line is 'test@intro:~$ done;1553743085'
            left_dollar_part, right_dollar_part = line.split('$',1)
            current_working_directory = left_dollar_part.split(':',1)[-1]
            current_working_directory = current_working_directory.replace('~', ttylog_sessions[current_session_id]['home_dir'] ,1)
            user_prompt = ttylog_sessions[current_session_id]['initial_prompt']
            right_dollar_part = right_dollar_part[1:]

            #Incase the user closes the terminal, without using the 'exit' command, line is like 'test@intro:~$'
            if len(right_dollar_part) == 0:
                continue

            line_split = right_dollar_part.split(';')

            if line_split[-1].isdigit():
                line_timestamp = int(line_split[-1])
                line_command = ';'.join(line_split[:-1] )
            else:
                line_timestamp = 0

            #line_timestamp = int(line_split[-1])
            #line_command = ';'.join(line_split[:-1] )
            continue

        elif root_prompt.casefold() in line.casefold():
            #Same line is 'google]0;root@intro: ~root@intro:~# done;1554092159'
            start_of_first_prompt = line.casefold().find(root_prompt.casefold() )
            if start_of_first_prompt > 0:
                output_till_start_of_prompt = line[:start_of_first_prompt]
                output_prevous_command += output_till_start_of_prompt + "\n"
                line = line[start_of_first_prompt:]

            # start_of_last_prompt = line.rfind(root_prompt)
            # line = line[start_of_last_prompt:]

            if line_timestamp > 0 and len(line_command) > 0:
                #If this is the first line when the user became root, we want the prompt to be 'user_prompt', not 'root_prompt'
                if is_current_prompt_root == False:
                    user_prompt = ttylog_sessions[current_session_id]['initial_prompt']
                    ttylog_sessions[current_session_id]['lines'].append(['CMBEGIN', node_name, line_timestamp, current_working_directory, line_command, output_prevous_command, user_prompt])
                    is_current_prompt_root = True
                else:
                    ttylog_sessions[current_session_id]['lines'].append(['CMBEGIN', node_name, line_timestamp, current_working_directory, line_command, output_prevous_command, root_prompt])
                line_timestamp = 0
                line_command = ''
            
            output_prevous_command = ''

            left_hash_part, right_hash_part = line.split('#',1)
            current_working_directory = left_hash_part.split(':',1)[-1]
            current_working_directory = current_working_directory.replace('~', root_home_dir ,1)
            right_hash_part = right_hash_part[1:]

            #Incase the user closes the terminal, without using the 'exit' command, line is like 'test@intro:~$'
            if len(right_hash_part) == 0:
                continue
                
            line_split = right_hash_part.split(';')
            
            if line_split[-1].isdigit():
                line_timestamp = int(line_split[-1])
                line_command = ';'.join(line_split[:-1] )
            else:
                line_timestamp = 0
            
            #line_timestamp = int(line_split[-1])
            #line_command = ';'.join(line_split[:-1] )
            continue



        #Get the session exit line
        elif r'END tty_sid' in line:
            if line_timestamp > 0 and len(line_command) > 0:
                if is_current_prompt_root == True:
                    ttylog_sessions[current_session_id]['lines'].append(['CMBEGIN', node_name, line_timestamp, current_working_directory, line_command, output_prevous_command, root_prompt])
                    is_current_prompt_root = False
                ttylog_sessions[current_session_id]['lines'].append(['CMBEGIN', node_name, line_timestamp, current_working_directory, line_command, output_prevous_command, user_prompt])
                line_timestamp = 0
                line_command = ''
            
            output_prevous_command = ''
            continue

        #Get the Command Output line
        elif ttylog_sessions[current_session_id]['initial_prompt'].casefold() not in line.casefold() and root_prompt.casefold() not in line.casefold() :
            output_prevous_command += line + "\n"

    #Combining the ttylogs for all the sessions, and Sorting the ttylog lines by time
    sorted_ttylog_lines = []
    for session in ttylog_sessions.values():
        #If there was a session, with no user entered line. That is, that ttylog session just had the first 3 lines, for 'starting session', 'User prompt', and 'Home directory'
        if 'lines' not in session:
            continue
        for line in session['lines']:
            sorted_ttylog_lines.append(line)

    sorted_ttylog_lines.sort(key = sort_ttylog_lines)

    #Writing data to CSV
    csvfile = open(csv_output_file,'w', newline='')
    csvwriter = csv.writer(csvfile, delimiter=',', quotechar='%', quoting=csv.QUOTE_MINIMAL)

    for line in sorted_ttylog_lines:
        csvwriter.writerow(line)

    csvfile.close()
