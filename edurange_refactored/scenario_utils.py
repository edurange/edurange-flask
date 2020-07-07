import os
import yaml
from flask import session

from edurange_refactored.user.models import Scenarios

class CatalogEntry:
    def __init__(self, name, description):
        self.name = name
        self.description = description

def create_scenario(name, infoFile, owner, group):
    name = name.join(e for e in name if e.isalnum())
    desc = 'Getting Started'
    own_id = session.get('_user_id')
    Scenarios.create(name=name, description=desc, owner_id=own_id)

    os.mkdir('./data/tmp/' + name)
    os.chdir('./data/tmp/' + name)

#copy_directory('scenarios/templates/' + SELECTION, os.curdir)

    with open('example.tf', 'w') as f:
        f.write("""provider "docker" {}
provider "template" {}

resource "docker_container" """ + "\""+ name + "\"" """ {
  name = """ + "\""+ name + "\"" """
  image = "rastasheep/ubuntu-sshd:18.04"
  restart = "always"
  hostname  = "NAT"

  connection {
    host = self.ip_address  
    type = "ssh"
    user = "root"
    password = "root"
  }

  ports {
    internal = 22
  }

  provisioner "remote-exec" {
    inline = [
    "useradd --home-dir /home/jack --create-home --shell /bin/bash --password $(echo passwordfoo | openssl passwd -1 -stdin) jack",
    ]
  }
}""")

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


