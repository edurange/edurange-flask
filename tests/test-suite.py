#!/usr/bin/env python3
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
        logger.success(f'🚀 Scenario is ready to be played!')
        return 0
    else:
        logger.error(f'⛔️ {user_count - users_passed} users failed some test')
        return 1


def get_tests():
    global tests, test_count

    with open(f'{DIRECTORY}/tests.json') as fd:
        dump = fd.read()

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
    config = config['outputs'][f'{SCENARIO}_nat']['value'][0]['ip_address_public'].split(':')

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
        success = test['success'].replace('$USERNAME$', username)

        logger.info(f'\t⚙️  Testing {test["name"]}...')

        output = run(test['command'])

        if output == success:
            tests_passed += 1
        else:
            logger.warning(f'\t\t❗️ Failed test for {test["name"]}')

    if tests_passed == test_count:
        return True
    else:
        logger.error(f'❌ User {username} failed {test_count - tests_passed} test(s)')
        return False


def run(command):
    """Return the first line of output of the command. Trims the new line byte."""
    stdin, stdout, stderr = ssh.exec_command(command)

    return stdout.readlines()[0][:-1]


if __name__ == '__main__':
    logger.remove()
    logger.add(sys.stdout, colorize=True, format=
        '<green>{time:MM-DD HH:mm:ss.SSS}</green> | <level>{message}</level>'
    )

    if len(sys.argv) < 2:
        print(f'Usage: {sys.argv[0]} <scenario>')
        sys.exit(1)

    SCENARIO = sys.argv[1]

    # TODO: check if scenario directory exists
    DIRECTORY = f'{os.environ["HOME"]}/edurange-flask/data/tmp/{SCENARIO}'

    try:
        main()
    except KeyboardInterrupt:
        logger.critical(f'Stopped at CTRL-C')
        ssh.close()
    except Exception as e:
        logger.critical(f'Crashed at error: {e}')
