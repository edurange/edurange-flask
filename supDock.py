
import docker
import os
import json

            
def askDock(scenario_uniqueName):

    dockClient = docker.from_env()
    active_containers = dockClient.containers.list()

    dockList = []

    for i in range(len(active_containers)):

        attrs = active_containers[i].attrs
        dockName = attrs["Name"]
        dockName = dockName[1:] #slice off the /

        if (dockName == scenario_uniqueName):
            print(attrs['NetworkSettings']['Ports']['22/tcp'][0]["HostPort"])
            return attrs['NetworkSettings']['Ports']['22/tcp'][0]["HostPort"]

askDock('sshinc1_FourthStop')

# some notes:  it seems like the process that is currently getting the IP and port for the active
# correct container is getting info that is not always the same as the
# value obtained by askDock().  this is not confirmed.

# next step is to confirm case

# def item_generator(json_input, lookup_key):
#     if isinstance(json_input, dict):
#         for k, v in json_input.items():
#             if k == lookup_key:
#                 yield v
#             else:
#                 yield from item_generator(v, lookup_key)
#     elif isinstance(json_input, list):
#         for item in json_input:
#             yield from item_generator(item, lookup_key)

# def identify_state(name, state):
#     if state == "Stopped":
#         return {"Nothing to show": "Scenario is Not Running"}
#     addresses = {}
#     c_names = []
#     name = "".join(e for e in name if e.isalnum())
#     if os.path.isdir(os.path.join("./data/tmp/", name)):
#         try:
#             state_file = open("./data/tmp/" + name + "/terraform.tfstate", "r")
#             data = json.load(state_file)

#             containers = item_generator(data, "name")
#             for c in list(containers):
#                 if c != "string" and c not in c_names:
#                     c_names.append(c)

#             public_ips = item_generator(data, "ip_address_public")
#             miss = 0
#             for i, a in enumerate(list(public_ips)):
#                 if a != "string":
#                     addresses[c_names[i - miss]] = a
#                 else:
#                     miss += 1

#             return addresses

#         except FileNotFoundError:
#             return {
#                 "No state file found": "Has the scenario been started at least once?"
#             }
#         except json.decoder.JSONDecodeError:
#             return {"State file is still being written": "Try Refreshing"}

#     else:
#         return {"Could not find scenario folder": "Please destroy and re-make this scenario"}