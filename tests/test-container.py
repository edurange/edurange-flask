#!/usr/bin/env python3
import argparse
import json
import os
import sys

import paramiko
from loguru import logger


def main():
    get_tests()
    logger.info(f'[i] Loaded {test_count} tests')

    credentials = get_credentials()

    users_passed, user_count = 0, len(credentials)
    logger.info(f'[i] Fetched credentials for {user_count} users')

    set_connection_details()
    logger.info(f'[i] HOST = {HOST}; PORT = {PORT}')

    for credential in credentials:
        username, password = credential[0]['username'], credential[0]['password']
        connect_to_container(username, password)

        if run_tests(username):
            users_passed += 1
            logger.success(f'✅ [{users_passed}/{user_count}] {username} passed all tests')

        ssh.close()  # Disconnect from container

    if users_passed == user_count:
        logger.success(f'🎉🎉🎉 All {user_count} users passed all {test_count} tests')
        logger.success(f'🚀 {SCENARIO} is ready to be played!')
        return 0
    else:
        logger.error(f'⛔️ {user_count - users_passed} users failed some test')
        return 1


def get_tests():
    global tests, test_count

    try:
        with open(f'{ROOT}/scenarios/prod/{TYPE}/tests.json') as fd:
            dump = fd.read()
    except FileNotFoundError:
        logger.error(f'Make sure a well-defined tests.json file is at scenarios/prod/{TYPE}')
        sys.exit(1)

    tests = json.loads(dump)
    test_count = len(tests)


def get_credentials():
    with open(f'{DIRECTORY}/students.json') as fd:
        dump = fd.read()

    return json.loads(dump).values()


def set_connection_details():
    global HOST, PORT

    with open(f'{DIRECTORY}/terraform.tfstate') as fd:
        dump = fd.read()

    config = json.loads(dump)

    try:
        if 'TotalRecon' in SCENARIO:
            label = f'{SCENARIO}_Home'
        else:
            label = f'{SCENARIO}_nat'

        config = config['outputs'][label]['value'][0]['ip_address_public'].split(':')

    except KeyError:
        logger.critical(f'Make sure {SCENARIO} is started')
        sys.exit(1)

    HOST, PORT = config[0], config[1]


def connect_to_container(username, password):
    global ssh

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(HOST, PORT, username, password)

    logger.info(f'[i] Logged into {username}\'s container...')


def run_tests(username):
    tests_passed = 0

    for test in tests:
        logger.info(f'\t⚙️  Testing {test["name"]}...')

        # Determine if the test's success is single or multi-line.
        if type(test['success']) == str:
            single_line_output = True
            success = test['success'].replace('$USERNAME$', username)
        else:
            single_line_output = False
            success = [line.replace('$USERNAME$', username) for line in test['success']]

        output = run(test['command'], single_line_output)

        if output == success:
            tests_passed += 1
        else:
            logger.warning(f'\t\t❗️ Failed test for {test["name"]}')

    if tests_passed == test_count:
        return True
    else:
        logger.error(f'❌ User {username} failed {test_count - tests_passed} test(s)')
        return False


def run(command, single_line_output):
    """Return the command's output trimming the new line byte of all lines.

    Args:
        command (string): The command to be run.
        single_line_output (boolean): If the command's output is single or multi-line.

    Returns:
        string|list: The output of the command.
    """

    stdin, stdout, stderr = ssh.exec_command(command)

    output = stdout.readlines()

    if single_line_output:
        return output[0][:-1]  # Only first line of output.

    return [line[:-1] for line in output]  # Trim all lines.


if __name__ == '__main__':
    logger.remove()
    logger.add(sys.stdout, colorize=True, format=
        '<green>{time:MM-DD HH:mm:ss.SSS}</green> | <level>{message}</level>'
    )

    parser = argparse.ArgumentParser(description='Test the containers of a scenario.')

    parser.add_argument('scenario', help='scenario name')
    parser.add_argument('--type', required=True,
        choices=['file_wrangler', 'getting_started'], help='scenario type'
    )

    args = parser.parse_args()

    SCENARIO, TYPE = args.scenario, args.type

    ROOT = F'{os.environ["HOME"]}/edurange-flask'
    DIRECTORY = f'{ROOT}/data/tmp/{SCENARIO}'

    if not os.path.isdir(DIRECTORY):
        logger.error(f'Make sure the {SCENARIO} exists and its folder is in data/tmp/')
        sys.exit(1)

    try:
        main()
    except KeyboardInterrupt:
        logger.warning(f'Stopped at CTRL-C')
        ssh.close()
