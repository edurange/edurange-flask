import os
import yaml


class CatalogEntry:
    def __init__(self, name, description):
        self.name = name
        self.description = description


def populate_catalog():
    scenarios = [dI for dI in os.listdir('./scenarios/prod/') if os.path.isdir(os.path.join('./scenarios/prod/', dI))]
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


def begin_tf_and_write_providers(name):
    with open(name + '.tf', 'w') as tf:
        tf.write(
            """
provider "docker" {}
provider "template" {}
""")


def write_bash(tf, filenames):
    for f in filenames:
        tf.write("""
  provisioner "file" {
    source      = "${path.module}/../../../scenarios/""" + f + "\"" + "\n" + """
    destination = """ + "\"/" + f + "\"\n" + """
  }
""")


def write_users(tf, usernames, passwords):
    for i, name in enumerate(usernames):
        tf.write("""
      "useradd --home-dir /home/""" + name
            + """ --create-home --shell /bin/bash --password $(echo """ + passwords[i]
            + """ | openssl passwd -1 -stdin) """ + name + "\","
                 )


def write_run_scripts(tf, filenames):
    for f in filenames:
        tf.write(
            """
      "chmod +x /""" + f + "\"" + """,
      "mv /""" + f + " /usr/bin/" + f + "\"" + """,
"""
        )


def begin_code_block(tf):
    tf.write(
        """
  provisioner "remote-exec" {
    inline = [
"""
    )
    return


def end_code_block(tf):
    tf.write(
        """
    ]   
  }      
}
""")


def write_container(name, usernames, passwords, filenames):
    with open(name + '.tf', 'a') as tf:
        tf.write(
            """ 
resource "docker_container" """ + "\"" + name + "\"" """ {
  name = """ + "\"" + name + "\"" """
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
        """
        )

        write_bash(tf, filenames)

        begin_code_block(tf)

        write_users(tf, usernames, passwords)

        write_run_scripts(tf, filenames)

        end_code_block(tf)
