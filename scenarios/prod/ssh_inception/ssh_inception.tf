resource "docker_network" "SNAME_NAT" {
  name = "SNAME_NAT"
  driver = "bridge"
  internal = "false"
  ipam_config {
    subnet = "10.0.1.0/27"
  }
}


resource "docker_network" "SNAME_PLAYER" {
  name = "SNAME_PLAYER"
  driver = "bridge"
  internal = "true"
  ipam_config { 
    subnet = "10.0.0.0/27"
  }
}

resource "docker_container" "SNAME_nat" {
  name = "SNAME_nat"
  image = "sanivo/edurange_alpine:latest"
  restart = "always"
  hostname  = "NAT"

  connection {
    host = self.ports[0].ip
    port = self.ports[0].external
    type = "ssh"
    user = "root"
    password = "sup3r_s3cr3t_r00t_p4ssw0rd"
  }

  ports {
    internal = 22
  }
 
  capabilities {
    add = ["NET_ADMIN"]
  }

  networks_advanced {
    name = "SNAME_NAT"
    ipv4_address = "10.0.1.2"
  }

  networks_advanced {
    name = "SNAME_Player"
    ipv4_address = "10.0.0.2"
  }
  command = ["/usr/sbin/sshd", "-D"]

  
  provisioner "remote-exec" {
    inline = [
      "echo -e 'passwordfoo123\npasswordfoo123' | adduser student",
    ]
  }
}

resource "docker_container" "SNAME_First_Stop" {
  name = "SNAME_First_Stop"
  image = "sanivo/edurange_alpine:latest"
  restart = "always"
  hostname = "First_Stop"

  connection {
    host = self.ports[0].ip
    port = self.ports[0].external
    type = "ssh"
    user = "root"
    password = "sup3r_s3cr3t_r00t_p4ssw0rd"
  }

  ports {
    internal = 22
    ip = "10.0.0.2"
  }
  
  capabilities {
    add = ["NET_ADMIN"]
  }

  networks_advanced {
    name = "SNAME_Player"
    ipv4_address = "10.0.0.5"
  }
  command = ["/usr/sbin/sshd", "-D"]







}
