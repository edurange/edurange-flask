import os
import yaml
from flask import session
from edurange_refactored.user.models import Scenarios


class CatalogEntry:
    def __init__(self, name, description):
        self.name = name
        self.description = description


def populate_catalog():
    scenarios = [dI for dI in os.listdir('./scenarios/prod/') if os.path.isdir(os.path.join('./scenarios/prod/',dI))]
    descriptions = []

    for s in scenarios:
        with open('./scenarios/prod/' + s + '/' + s + '.yml', 'r') as yml:
            document = yaml.full_load(yml)
            for item, doc in document.items():
                if item == 'Description':
                    descriptions.append(doc)
    entries = []
    for i in range(len(scenarios)):
        entries.append(CatalogEntry(scenarios[i].title(), descriptions[i]))
    return entries


