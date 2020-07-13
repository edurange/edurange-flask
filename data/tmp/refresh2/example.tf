provider "docker" {}
    provider "template" {}
    
    resource "docker_container" "refresh2" {
      name = "refresh2"
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
    }