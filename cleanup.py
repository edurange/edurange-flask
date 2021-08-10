# '''
# This script catches the interrupt signal made by pressing ctrl+c in order to perform cleanup tasks (such as destroying terraform instances)

# Adapted from https://stackoverflow.com/questions/1112343/how-do-i-capture-sigint-in-python

# Apollo Heidal
# '''
import signal
import sys
import os
import time

# wait for flask to save and close db connection
time.sleep(1)

def sigint_handler(sig, frame):
    current_dir = os.getcwd()
    scenarios_dir = current_dir + "/data/tmp"

    print(os.getcwd())
    print("caught sigint!")

    for scenario in os.listdir(scenarios_dir):
        os.chdir(scenarios_dir + "/" + scenario)
        print(os.getcwd())
        os.system("terraform destroy --auto-approve")

    os.system("sudo -u postgres bash -c \"psql --dbname=namefoo -c \"update scenarios set status=0 where status=1;\"\"")
    sys.exit()


signal.signal(signal.SIGINT, sigint_handler)
signal.pause()

# sudo -u postgres bash -c "psql --dbname=namefoo -c \"select name,id from scenarios where status=1;\""

# update scenarios set status=0 where status=1;

# length=$(sudo -u postgres bash -c "psql --dbname=namefoo -c \"select name from scenarios where status=0;\"" | awk 'END {print NR, $1}')

# sudo -u postgres bash -c "psql --dbname=namefoo --tuples-only --command=\"select name from scenarios where status=0;\" | awk '{print}'"


### from autoapp.py
# @app.teardown_appcontext
# def cleanup():
# if os.environ["FLASK_DEBUG"] == "0":
#     import signal, sys
#     from time import sleep

#     def sigint_handler(a, b):
#         print("Running scenario cleanup...")
#         with app.test_request_context():
#             active_scenarios = Scenarios.query.all()

#             for s in active_scenarios:
#                 if s.status == 1:
#                     print(f"stopping {s.name} scenario")
#                     stop(s.id)
        
#         sys.exit()

#     signal.signal(signal.SIGINT, sigint_handler)

# @app.teardown_appcontext
# def exit_handler(a):
#     if os.environ["FLASK_DEBUG"] == "0":
#         print("no debug")
#         active_scenarios = Scenarios.query.all()
#         for s in active_scenarios:
#             if s.status == 1:
#                 print(f"stopping {s.name} scenario")
#                 stop(s.id)
#     else:
#         print("debug")


### from app.py
# def register_cleanup(app):
#     if os.environ["FLASK_DEBUG"] == "0":
#         def sigint_handler(a, b):
#             print("Running scenario cleanup...")

#             active_scenarios = Scenarios.query.all()

#             for s in active_scenarios:
#                 if s.status == 1:
#                     print(f"stopping {s.name} scenario")
#                     stop(s.id)
#                     sleep(1)

#         signal.signal(signal.SIGINT, sigint_handler)