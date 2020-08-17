import os
import shutil
import json


def find_and_copy_template(s_type, c_name):
    path = '../../../scenarios/prod/' + s_type
    try:
        shutil.copy(path + '/' + c_name + '.tf.json', c_name + '.tf.json')
    except FileNotFoundError:
        return "Template not found, or path error"


def build_users(usernames, passwords):
    users = []
    for i, u in enumerate(usernames):
        next_line = ""
        if i != 0:
            next_line += "\""
        next_line += str("echo -e '" + str(passwords[i]) + "\\n" + str(passwords[i]) + "' | adduser " + u)
        if i != len(usernames) - 1:
            next_line += "\","
        users.append(next_line)
    return users


def build_uploads(s_files, g_files, u_files, s_type):
    all_files = s_files + g_files + u_files
    uploads = ""
    for f in all_files:
        uploads += str("""
  "provisioner": [
    { 
    "file": [ 
      {
      "source"      : "${path.module}/../../../scenarios/prod/""" + s_type + "/" + f + '",'
                       + """
      "destination" : """ + '"/' + f + '"'
                       + """
      }
    ]
    }
  ],
""")
    return uploads


def build_execute_files(s_files, g_files, u_files):
    execs = "mkdir /home/ubuntu\",\n"
    execs += "\"apk add bash\",\n"

    for i, f in enumerate(g_files):
        execs += str("\"chmod +x /" + f + '"' + """, 
        "mv /""" + f + " /usr/bin/" + f + '",\n')

    for i, f in enumerate(u_files):
        execs += str("""
      "chmod +rwx /""" + f + '"' + """,
      "cp -R /""" + f + " /home/ubuntu/" + f + '"' + """,
""")
    for i, f in enumerate(s_files):
        execs += str("""
      "chmod +x /""" + f + '"' + """,
      "mv /""" + f + " /home/ubuntu/" + f + '"' + """,
      "bash /home/ubuntu/""" + f)
        if i != len(s_files) - 1:
            execs += "\","
    return execs


def adjust_network(address, name):
    try:
        net = open('network.tf.json', 'r+')
        net_config = json.load(net)
    except FileNotFoundError:
        return "Network Template Not Found"

    # Replace the name and addresses in the 'network' file
    for i, r in enumerate(net_config['resource']):
        for s in r:
            for j, t in enumerate(net_config['resource'][i][s]):
                net_config['resource'][i][s][j] = eval(str(t).replace('SNAME', name).replace('OCTET', address))
    with open('tmp.tf.json', 'w') as f:
        json.dump(net_config, f, indent=4)

    os.rename('tmp.tf.json', 'network.tf.json')


def write_resource(address, name, s_type,
                   c_name, usernames, passwords,
                   s_files, g_files, u_files):
    # Generate a list of strings of commands for adding users
    users = build_users(usernames, passwords)

    # Generate a list of 'provisioner' blocks to upload all files
    uploads = build_uploads(s_files, g_files, u_files, s_type)

    # Generate a list of commands to move files, and run them if needed
    execs = build_execute_files(s_files, g_files, u_files)

    # Make sure the container has a known template
    try:
        tf = open(c_name + '.tf.json', 'r+')
        config = json.load(tf)
    except FileNotFoundError:
        return "Template not found"

    # SNAME and OCTET appear in multiple places, so this 'for' loop is used to replace all occurrences of them.
    # To inspect the structure of the 'config', use 'flask shell', import json, and load the data as in the above 'try'
    for i, r in enumerate(config['resource']):
        for s in r:
            for j, t in enumerate(config['resource'][i][s]):
                config['resource'][i][s][j] = eval(str(t).replace('SNAME', name).replace('OCTET', address))

    for i, l in enumerate(config['locals']):
        config['locals'][i] = eval(str(l).replace('SNAME', name))

    for i, o in enumerate(config['output']):
        config['output'][i] = eval(str(o).replace('SNAME', name))

    # Use a temporary file to hold the updated data
    with open('tmp.tf.json', 'w') as f:
        json.dump(config, f, indent=4)

    # Move the temporary file, replacing the template
    os.rename('tmp.tf.json', c_name + '.tf.json')

    # Read our new file as raw text
    with open(c_name + '.tf.json', 'r') as outfile:
        data = outfile.read()

    # Insert the list of commands that register students in the 'remote-exec' block
    data = data.replace('USERS', '\n'.join(users))

    # Find the first 'provisioner', insert more in the space prior to it for uploading files
    data = data[:data.index('provisioner') - 2] + uploads + data[data.index('provisioner') - 2:]

    # In the 'remote-exec' block, insert commands for moving and executing scenario files
    data = data.replace('EXECS', execs)

    print(data)

    with open(c_name + '.tf.json', 'w') as outfile:
        outfile.write(data)
