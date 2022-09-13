import json
import os

from random import shuffle, seed
import yaml
from flask import flash
from edurange_refactored.settings import KNOWN_SCENARIOS
from edurange_refactored.user.models import GroupUsers, ScenarioGroups
from edurange_refactored.database import db

# Import the scenario string, and set to 'known_types' as a list
known_types = KNOWN_SCENARIOS

# Old methodology for declaring 'known' scenarios

# known_types = [
#     "Elf_Infection",
#     "File_Wrangler",
#     "Getting_Started",
#     "Metasploitable",
#     "Ransomware",
#     "Ssh_Inception",
#     "Strace",
#     "Total_Recon",
#     "Treasure_Hunt",
#     "Web_Fu"
# ]


class CatalogEntry:
    def __init__(self, name, description):
        self.name = name
        self.description = description


def populate_catalog():
    scenarios = [
        dI
        for dI in os.listdir("./scenarios/prod/")
        if os.path.isdir(os.path.join("./scenarios/prod/", dI))
    ]
    descriptions = []

    for s in scenarios:
        with open("./scenarios/prod/" + s + "/" + s + ".yml", "r") as yml:
            document = yaml.full_load(yml)
            for item, doc in document.items():
                if item == "Description":
                    descriptions.append(doc)
    entries = []
    for i in range(len(scenarios)):
        entries.append(CatalogEntry(scenarios[i].title(), descriptions[i]))
    return entries


def item_generator(json_input, lookup_key):
    if isinstance(json_input, dict):
        for k, v in json_input.items():
            if k == lookup_key:
                yield v
            else:
                yield from item_generator(v, lookup_key)
    elif isinstance(json_input, list):
        for item in json_input:
            yield from item_generator(item, lookup_key)


def gather_files(s_type, logger):
    c_names = []
    g_files = []
    s_files = []
    u_files = []
    package_list = []
    ip_addrs = []

    if os.path.isdir(os.path.join("./scenarios/prod/", s_type)):
        logger.info("Scenario of type {} Found".format(s_type))
        logger.info("Now attempting to load file requirements...")
        try:
            with open(
                os.path.join("./scenarios/prod/", s_type + "/" + s_type + ".json")
            ) as f:
                data = json.load(f)

                containers = item_generator(data, "name")
                for i in containers:
                    c_names.append(i)

                logger.info("Found containers: {}".format(c_names))

                global_files = item_generator(data, "global_files")
                for g in list(global_files):
                    g_files.append(g)

                logger.info("Found global files: {}".format(g_files))

                system_files = item_generator(data, "system_files")
                for s in list(system_files):
                    s_files.append(s)

                logger.info("Found system files: {}".format(s_files))

                user_files = item_generator(data, "user_files")
                for u in list(user_files):
                    u_files.append(u)

                logger.info("Found user files: {}".format(u_files))

                packages = item_generator(data, "packages")
                for p in list(packages):
                    package_list.append(p)

                logger.info("Found required packages: {}".format(package_list))

                ip_addresses = item_generator(data, "ip_address")
                for a in list(ip_addresses):
                    ip_addrs.append(a)

                logger.info("Found addresses: {}".format(ip_addrs))

                return c_names, g_files, s_files, u_files, package_list, ip_addrs

        except FileNotFoundError:
            logger.warn("Could Not load json file for type: {}".format(s_type))
            raise FileNotFoundError

    else:
        logger.warn("Invalid Scenario Type - Folder Not Found")
        raise Exception(f"Could not correctly identify scenario type")


def identify_type(form):
    found_type = ""

    for i, s_type in enumerate(known_types):
        if s_type in form.keys():
            found_type = s_type

    return found_type


def identify_state(name, state):
    if state == "Stopped":
        return {"Nothing to show": "Scenario is Not Running"}
    addresses = {}
    c_names = []
    name = "".join(e for e in name if e.isalnum())
    if os.path.isdir(os.path.join("./data/tmp/", name)):
        try:
            state_file = open("./data/tmp/" + name + "/terraform.tfstate", "r")
            data = json.load(state_file)

            containers = item_generator(data, "name")
            for c in list(containers):
                if c != "string" and c not in c_names:
                    c_names.append(c)

            public_ips = item_generator(data, "ip_address_public")
            miss = 0
            for i, a in enumerate(list(public_ips)):
                if a != "string":
                    addresses[c_names[i - miss]] = a
                else:
                    miss += 1

            return addresses

        except FileNotFoundError:
            return {
                "No state file found": "Has the scenario been started at least once?"
            }
        except json.decoder.JSONDecodeError:
            return {"State file is still being written": "Try Refreshing"}

    else:
        return {"Could not find scenario folder": "Please destroy and re-make this scenario"}

def query_valid_scenario_id(id, session):
    scenId = session.query(Scenarios).get(id)
    return scenId


def gen_chat_names(sid: int): 
    """
    Synopsis
    --------
    Return a mapping of student IDs to temporary anonymous chat usernames.
    One name is created as <adjective><Noun> in camel case. Assumes the number of 

    Parameters
    ----------
    sid : int
        Scenario id

    Returns
    -------
    dict
        Dictionary of {student ID : chatname} mappings
    
    """
    # Save the db session as a variable
    session = db.session

    nouns = [
            "Animal",      "Horse",     "Parrot",   "Rainbow",    "Lizard",
            "Ghost",       "Oyster",    "Potato",   "Fish",       "Lion",
            "Kangaroo",    "Rocket",    "Engine",   "Magician",   "Tractor",
            "Poetry",      "Piano",     "Finger",   "Ambassador", "Boxer",
            "Goldsmith",   "Scavenger", "Surgeon",  "Chemist",    "Cobra",
            "Elk",         "Wolf",      "Tiger",    "Shark",      "Otter",
            "Fox",         "Falcon",    "Badger",   "Bear",       "Raven",
            "Rabbit",      "Hare",      "Ant",      "Scorpion",   "Owl",
            "Finch",       "Starling",  "Sparrow",  "Bulldozer",  "Astronomer",
            "Philosopher", "Engineer",  "Catfish",  "Pirate",     "Bilder",
            "Captain",     "Sailor",    "Cactus",   "Genie",      "Chimera",
            "Banshee",     "Dragon",    "Pheonix",  "Basilisk",   "Griffin",
            "Centaur",     "Sprite",    "Golem",    "Sphinx",     "Moose",
            "Mongoose",    "Star",      "Starfish", "Comet",      "Argonaut"
        ]

    adjectives = [
        "blue",          "fast",       "squirrely",     "round",
        "extravagant",   "orange",     "red",           "small",
        "rotund",        "supreme",    "inconspicuous", "fancy",
        "enraging",      "unseen",     "proper",        "green",
        "fabulous",      "nostalgic",  "shy",           "large",
        "oblivious",     "obvious",    "extreme",       "unphased",
        "frightening",   "suspicious", "miniscule",     "enormous",
        "gigantic",      "pink",       "fuzzy",         "sleek",
        "fantastic",     "boring",     "colorful",      "loud",
        "quiet",         "powerful",   "focused",       "confusing",
        "skillful",      "purple",     "invisible",     "undecided",
        "calming",       "tall",       "flat",          "octagonal",
        "hexagonal",     "triangular", "robust",        "thorough",
        "surprising",    "unexpected", "whimsical",     "musical",
        "imaginary",     "squishy",    "intricate",     "complex",
        "uncomplicated", "efficient",  "hidden",        "sophisticated",
        "ridiculous",    "strong",     "turquoise",     "plentiful",
        "yodeling",      "sneaky"
    ]

    num_words = min(len(nouns), len(adjectives))

    # Shuffle the lists, seeded on the scenario id
    seed(sid)
    shuffle(nouns)
    shuffle(adjectives)

    # Get group id from scenario id
    gid = session\
                    .query(ScenarioGroups.group_id)\
                    .filter(ScenarioGroups.scenario_id == sid)\
                    .first()[0]
    # Get list of student ids from group id
    student_ids = session\
                    .query(GroupUsers.id)\
                    .filter(GroupUsers.group_id == gid)\
                    .all()

    # Collect only the useful part of the DB query
    # Reduce the ids by the number of words to allow indexing
    student_ids = map(lambda row: row[0] % num_words, student_ids)
    
    return {id: adjectives[id] + nouns[id] for id in student_ids}
    