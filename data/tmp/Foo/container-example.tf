variable "students" {
  type = list(object({
    login              = string,
    password           = object({ plaintext = string, hash = string }),
    variables          = object({
      follow_me_filename = string,
      super_secret       = string
    })
  }))
  description = "list of players"
  default = []
}

provider "docker" {}
provider "template" {}

resource "docker_network" "SubnetNAT" {
  name = "SubnetNAT"
  driver = "bridge"
  internal = "false"
  ipam_config {
    subnet = "10.0.1.0/27"
  }
}

resource "docker_container" "nat" {
  name = "nat"
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

  networks_advanced {
    name = "SubnetNAT"
    ipv4_address = "10.0.1.2"
  }



  provisioner "file" {
    source      = "${path.module}/images"
    destination = "/home/ubuntu"
  }

  provisioner "file"{
    source = "${path.module}/stuff"
    destination = "/home/ubuntu"
  }

  provisioner "file" {
    source      = "${path.module}/toLearn"
    destination = "/home/ubuntu"
  }

  provisioner "file" {
    source      = "${path.module}/final-mission"
    destination = "/home/ubuntu"
  }

  provisioner "file" {
    source = "${path.module}/setup_home"
    destination = "/home/ubuntu/setup_home"
  }
  provisioner "file"{
    source = "${path.module}/motd_nat"
    destination = "/home/ubuntu/motd_nat"
  }
  provisioner "file" {
    content = templatefile("${path.module}/install", {
      players = var.students
    })
    destination = "/home/ubuntu/install"
  }

  provisioner "remote-exec" {
    inline = [
    "useradd --home-dir /home/xennos --create-home --shell /bin/bash --password $(echo passwordfoo | openssl passwd -1 -stdin) xennos",
    "chmod +x /home/ubuntu/install",
    "chmod +x /home/ubuntu/setup_home",
    "chmod +x /home/ubuntu/motd_nat",
    "/home/ubuntu/motd_nat",
    "/home/ubuntu/install",
    ]
  }
}


locals {
  nat_extern = tostring(docker_container.nat.ports[0].external)
  host_addr =  "localhost"
}

output "instances" {
  value = [{
    name = "getting-started"
    ip_address_public = join(":", [local.host_addr, local.nat_extern])
  }]
}
