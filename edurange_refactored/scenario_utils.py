import json
import os

import yaml
from flask import flash

known_types = [
    "Ssh_Inception",
    "Strace",
    "Getting_Started",
    "Metasploitable",
    "File_Wrangler",
    "Total_Recon",
    "Treasure_Hunt",
    "Elf_Infection",
]


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


def begin_tf_and_write_providers(name):
    with open(name + ".tf", "w") as tf:
        tf.write(
            """
provider "docker" { host = "unix:///var/run/docker.sock"}
provider "template" {}
"""
        )


def write_global_files(tf, s_type, filenames):
    for f in filenames:
        tf.write(
            """
  provisioner "file" {
    source      = "${path.module}/../../../scenarios/""" + s_type + "/" + f + '"'
            + """
    destination = """ + '"/' + f + '"'
            + """
  }
"""
        )


def write_system_files(tf, s_type, filenames):
    for f in filenames:
        tf.write(
            """
  provisioner "file" {
    source      = "${path.module}/../../../scenarios/""" + s_type + "/" + f + '"'
            + """
    destination = """ + '"/' + f + '"'
            + """
  }
"""
        )


def write_user_files(tf, s_type, filenames):
    for f in filenames:
        tf.write(
            """
  provisioner "file" {
    source      = "${path.module}/../../../scenarios/""" + s_type + "/" + f + '"'
            + """
    destination = """ + '"/' + f + '"'
            + """
  }
"""
        )


def write_users(tf, usernames, passwords):
    for i, name in enumerate(usernames):
        tf.write(
            """
      "useradd --home-dir /home/""" + name
            + """ --create-home --shell /bin/bash --password $(echo """
            + passwords[i]
            + """ | openssl passwd -1 -stdin) """
            + name
            + '",\n'
        )


def write_make_dir(tf):
    tf.write("""
      "mkdir /home/ubuntu",
    """)


def write_run_global(tf, filenames):
    for f in filenames:
        tf.write(
            """
      "chmod +x /""" + f + '"' + """,
      "mv /""" + f + " /usr/bin/" + f + '"' + """,
"""
        )


def write_run_system(tf, filenames):
    for f in filenames:
        tf.write(
            """
      "chmod +x /""" + f + '"' + """,
      "mv /""" + f + " /home/ubuntu/" + f + '"' + """,
      "/home/ubuntu/""" + f + '"' + """,
"""
        )


def write_prep_user(tf, filenames):
    for f in filenames:
        tf.write(
            """
      "chmod +rwx /""" + f + '"' + """,
      "cp -R /""" + f + " /home/ubuntu/" + f + '"' + """,
"""
        )


def write_run_updates(tf, packages):
    tf.write(
        """
      "sed -i 's:^path-exclude=/usr/share/man:#path-exclude=/usr/share/man:' /etc/dpkg/dpkg.cfg.d/excludes",
      "apt-get update",
      "yes | apt-get install debconf-utils",
      "echo '* libraries/restart-without-asking boolean true' | debconf-set-selections",
      "yes | apt-get install """
        + " ".join(packages)
        + '"'
        + """,
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
"""
    )


def write_output_block(name, c_names):
    with open(name + '.tf', 'a') as tf:
        for c in c_names:
            c = name + "_" + c
            tf.write(
                """
  locals {
    """
    + c + """_extern = tostring(docker_container.""" + c + """.ports[0].external)
  }

  output """ + '"' + c + """" {
    value = [{
      name = """ + '"' + c + '"' + """
      ip_address_public = join(":", ["localhost", local.""" + c + """_extern])
    }]
  }
"""
            )


def write_network_nat(s_name):
    with open("network.tf", "w") as tf:
        tf.write( """
resource "docker_network" """ + "\"" + s_name + "_NAT\"" """ {
  name = """ + "\"" + s_name + "_NAT\"" """
  driver = "bridge"
  internal = "false"
}""")


def write_net_adv_nat(tf, s_name, ip):
    tf.write("""
  networks_advanced {
    name = """ + "\"" + s_name.split('_')[0] + "_NAT\"" """
  }
""")


def write_container(
    name, s_type, usernames, passwords, g_files, s_files, u_files, packages
):
    with open(name + ".tf", "a") as tf:
        tf.write(
            """
resource "docker_container" """ + "\"" + name + "\"" """ {
  name = """ + "\"" + name + "\"" """
  image = "rastasheep/ubuntu-sshd:18.04"
  restart = "always"
  hostname  = "NAT"

  connection {
    host = self.ports[0].ip
    port = self.ports[0].external
    type = "ssh"
    user = "root"
    password = "root"
  }

  ports {
    internal = 22
  }
        """
        )

        #if ip_addr is not None:
        #    write_net_adv(tf, name, ip_addr)

        s_type = "prod/" + s_type
        write_global_files(tf, s_type, g_files)

        write_system_files(tf, s_type, s_files)

        write_user_files(tf, s_type, u_files)

        begin_code_block(tf)

        #write_run_updates(tf, packages)

        write_users(tf, usernames, passwords)

        write_make_dir(tf)

        write_run_global(tf, g_files)

        write_prep_user(tf, u_files)

        write_run_system(tf, s_files)

        end_code_block(tf)



