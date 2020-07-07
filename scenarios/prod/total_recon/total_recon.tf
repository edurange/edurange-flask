variable "students" {
  type = list(object({
    login                  = string,
    password               = object({ plaintext = string, hash = string })
  }))
  description = "list of players in student group"
  default = [
    {
      login = "student"
      password = {
        plaintext = "password"
        hash      = "$6$jLRQrmzXweefgmfx$U1mJRBjSGTPH.kzHBqd32p4TQqYzsgH.UQPlkzmVUV/FCTcIZBh2erpsoe.5eTEYNYeD73ZvyJF.8Xsc1Jtli1"
      }
    }
  ]
}

variable "scenario_id" {
  type        = string
  description = "identifier for instance of this scenario"
  default     = "n/a"
}

variable "aws_access_key_id" {
  type = string
}

variable "aws_secret_access_key" {
  type = string
}

variable "aws_region" {
  type = string
}

variable "env" {
  type        = string
  default     = "development"
  description = "For example testing/development/production"
}

variable "owner" {
  type    = string
  default = "n/a"
}

output "instances" {
  value = [
    {
      name = "home"
      ip_address_public  = aws_instance.home.public_ip
      ip_address_private = aws_instance.home.private_ip
    },
    {
      name = "rekall"
      ip_address_private = aws_instance.rekall.private_ip
    },
    {
      name = "subway"
      ip_address_private = aws_instance.subway.private_ip
    },
    {
      name = "earth_spaceport"
      ip_address_private = aws_instance.earth_spaceport.private_ip
    },
    {
      name = "mars_spaceport"
      ip_address_private = aws_instance.mars_spaceport.private_ip
    },
    {
      name = "venusville"
      ip_address_private = aws_instance.venusville.private_ip
    },
    {
      name = "last_resort"
      ip_address_private = aws_instance.last_resort.private_ip
    },
    {
      name = "resistance_base"
      ip_address_private = aws_instance.resistance_base.private_ip
    },
    {
      name = "stealth_xmas"
      ip_address_private = aws_instance.stealth_xmas.private_ip
    },
    {
      name = "stealth_null"
      ip_address_private = aws_instance.stealth_null.private_ip
    },
    {
      name = "stealth_fin"
      ip_address_private = aws_instance.stealth_fin.private_ip
    }
  ]
}

locals {
  common_tags = {
    scenario_id   = var.scenario_id
    scenario_name = "total_recon"
    env           = var.env
    owner         = var.owner
    Name          = "total_recon" # By default tag every resource with total_recon, but this can be overwritten if that is not specific enough (eg there are more than one of that resource)
  }
}

provider "aws" {
  version    = "~> 2"
  profile    = "default"
  region     = "us-west-1"
  access_key = var.aws_access_key_id
  secret_key = var.aws_secret_access_key
}

provider "local" {
  version = "~> 1"
}

provider "tls" {
  version = "~> 2"
}

provider "template" {
  version = "~> 2"
}

provider "random" {
  version = "~> 2"
}

# find most recent official Ubuntu 18.04
data "aws_ami" "ubuntu" {
  most_recent = true

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-bionic-18.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  owners = ["099720109477"] # Canonical
}

# create ssh key pair
resource "tls_private_key" "key" {
  algorithm = "RSA"
  rsa_bits  = 4096
}

# upload the public key to aws
resource "aws_key_pair" "key" {
  key_name   = "total_recon/${var.scenario_id}"
  public_key = tls_private_key.key.public_key_openssh
}

# save the private key locally (useful for debugging)
resource "local_file" "key" {
  sensitive_content = tls_private_key.key.private_key_pem
  filename          = "id_rsa"

  provisioner "local-exec" {
    command = "chmod 600 id_rsa"
  }
}

locals {
  net_tools = ["nmap", "tshark", "iputils-ping", "net-tools"]
}

data "template_cloudinit_config" "home" {
  gzip          = true
  base64_encode = true

  part {
    filename     = "bash_history.cfg"
    content_type = "text/cloud-config"
    merge_type   = "list(append)+dict(recurse_list)"
    content = templatefile("${path.module}/bash_history.yml.tpl", {
      aws_key_id  = var.aws_access_key_id
      aws_sec_key = var.aws_secret_access_key
      scenario_id = var.scenario_id
      players     = var.students
    })
  }

  part {
    filename     = "init.cfg"
    content_type = "text/cloud-config"
    merge_type   = "list(append)+dict(recurse_list)"
    content = templatefile("${path.module}/cloud-init.yml", {
      players  = var.students
      packages = local.net_tools
      hostname = "home"
      motd     = file("${path.module}/motd_home")
      ip_addresses = []
    })
  }
}

resource "aws_instance" "home" {
  subnet_id                   = aws_subnet.home.id
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = "t2.small"
  private_ip                  = local.home_private_ip
  key_name                    = aws_key_pair.key.key_name
  associate_public_ip_address = true
  vpc_security_group_ids      = [
    aws_security_group.allow_all_internal.id,
    aws_security_group.ssh_ingress_from_world.id,
    aws_security_group.http_egress_to_world.id
  ]
  user_data_base64            = data.template_cloudinit_config.home.rendered

  tags = merge(local.common_tags, { Name = "total_recon/home" })

  connection {
    host        = self.public_ip
    type        = "ssh"
    user        = "ubuntu"
    private_key = tls_private_key.key.private_key_pem
  }
  provisioner "file" {
    source = "${path.module}/ttylog"
    destination = "/home/ubuntu/recon"
  }
  provisioner "file" {
    source = "${path.module}/tty_setup"
    destination = "/home/ubuntu/recon/tty_setup"
  }
  provisioner "remote-exec" {
    inline = [
      "cloud-init status --wait --long",
      "cd /home/ubuntu/recon",
      "sudo chmod +x tty_setup",
      "sudo ./tty_setup",
      "rm -rf /home/ubuntu/recon"
    ]
  }
}


data "template_cloudinit_config" "rekall" {
  gzip          = true
  base64_encode = true

  part {
    filename     = "bash_history.cfg"
    content_type = "text/cloud-config"
    merge_type   = "list(append)+dict(recurse_list)"
    content = templatefile("${path.module}/bash_history.yml.tpl", {
      aws_key_id  = var.aws_access_key_id
      aws_sec_key = var.aws_secret_access_key
      scenario_id = var.scenario_id
      players     = var.students
    })
  }

  part {
    filename     = "init.cfg"
    content_type = "text/cloud-config"
    merge_type   = "list(append)+dict(recurse_list)"
    content = templatefile("${path.module}/cloud-init.yml", {
      players  = var.students
      packages = local.net_tools
      hostname = "rekall"
      motd     = file("${path.module}/motd_rekall")
      ip_addresses = []
    })
  }

  part {
    filename     = "ssh_port_444"
    content_type = "text/x-shellscript"
    content = templatefile("${path.module}/change_ssh_port", {
      port: 444
    })
  }
}

resource "aws_instance" "rekall" {
  subnet_id                   = aws_subnet.earth.id
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = "t2.micro"
  private_ip                  = "10.0.0.4"
  key_name                    = aws_key_pair.key.key_name
  vpc_security_group_ids      = [
    aws_security_group.allow_all_internal.id,
    aws_security_group.http_egress_to_world.id
  ]
  user_data_base64            = data.template_cloudinit_config.rekall.rendered
  depends_on = [
    aws_nat_gateway.nat,
  ]
  tags = merge(local.common_tags, {
    Name = "total_recon/rekall"
  })

  connection {
    bastion_host        = aws_instance.home.public_ip
    bastion_port        = 22
    host                = self.private_ip
    port                = 444
    user                = "ubuntu"
    private_key         = tls_private_key.key.private_key_pem
  }

  provisioner "file" {
    source = "${path.module}/ttylog"
    destination = "/home/ubuntu/recon"
  }
  provisioner "file" {
    source = "${path.module}/tty_setup"
    destination = "/home/ubuntu/recon/tty_setup"
  }
  provisioner "remote-exec" {
    inline = [
      "cloud-init status --wait --long",
      "cd /home/ubuntu/recon",
      "sudo chmod +x tty_setup",
      "sudo ./tty_setup",
      "rm -rf /home/ubuntu/recon"
    ]
  }
}

data "template_cloudinit_config" "subway" {
  gzip          = true
  base64_encode = true

  part {
    filename     = "bash_history.cfg"
    content_type = "text/cloud-config"
    merge_type   = "list(append)+dict(recurse_list)"
    content = templatefile("${path.module}/bash_history.yml.tpl", {
      aws_key_id  = var.aws_access_key_id
      aws_sec_key = var.aws_secret_access_key
      scenario_id = var.scenario_id
      players     = var.students
    })
  }

  part {
    filename     = "init.cfg"
    content_type = "text/cloud-config"
    merge_type   = "list(append)+dict(recurse_list)"
    content = templatefile("${path.module}/cloud-init.yml", {
      players  = var.students
      packages = setunion(local.net_tools, ["apache2"])
      hostname = "subway"
      ip_addresses = []
      motd     = templatefile("${path.module}/motd_subway", {
        ip_address = local.earth_spaceport_private_ip
      })
    })
  }
}

# introduce some randomness so a different ip is used each time.

resource "random_integer" "subway_hostnum" {
  min     = 101
  max     = 252
}

resource "random_integer" "earth_spaceport_hostnum" {
  min     = 5
  max     = 100
}

resource "random_integer" "mars_spaceport" {
  min     = 192
  max     = 207
}

resource "random_integer" "venusville" {
  min     = 208
  max     = 232
}

resource "random_integer" "last_resort" {
  min     = 235
  max     = 249
}

locals {
  home_private_ip                 = "10.0.129.6"
  subway_private_ip               = cidrhost(aws_subnet.earth.cidr_block, random_integer.subway_hostnum.result)
  earth_spaceport_private_ip = cidrhost(aws_subnet.earth.cidr_block, random_integer.earth_spaceport_hostnum.result)
  mars_spaceport_private_ip  = "10.0.${random_integer.mars_spaceport.result}.33"
  venusville_private_ip           = "10.0.${random_integer.venusville.result}.64"
  last_resort_private_ip          = "10.0.${random_integer.last_resort.result}.144"
  resistance_base_private_ip      = "10.0.234.8"
}

resource "aws_instance" "subway" {
  subnet_id                   = aws_subnet.earth.id
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = "t2.micro"
  private_ip                  = local.subway_private_ip
  key_name                    = aws_key_pair.key.key_name
  vpc_security_group_ids      = [
    aws_security_group.allow_all_internal.id,
    aws_security_group.http_egress_to_world.id
  ]
  user_data_base64            = data.template_cloudinit_config.subway.rendered

  tags = merge(local.common_tags, { Name = "total_recon/subway" })

  connection {
    bastion_host        = aws_instance.home.public_ip
    host                = self.private_ip
    user                = "ubuntu"
    private_key         = tls_private_key.key.private_key_pem
  }

  provisioner "file" {
    source = "${path.module}/ttylog"
    destination = "/home/ubuntu/recon"
  }
  provisioner "file" {
    source = "${path.module}/tty_setup"
    destination = "/home/ubuntu/recon/tty_setup"
  }
  provisioner "remote-exec" {
    inline = [
      "cloud-init status --wait --long",
      "cd /home/ubuntu/recon",
      "sudo chmod +x tty_setup",
      "sudo ./tty_setup",
      "rm -rf /home/ubuntu/recon"
    ]
  }
}


data "template_cloudinit_config" "earth_spaceport" {
  gzip          = true
  base64_encode = true

  part {
    filename     = "bash_history.cfg"
    content_type = "text/cloud-config"
    merge_type   = "list(append)+dict(recurse_list)"
    content = templatefile("${path.module}/bash_history.yml.tpl", {
      aws_key_id  = var.aws_access_key_id
      aws_sec_key = var.aws_secret_access_key
      scenario_id = var.scenario_id
      players     = var.students
    })
  }

  part {
    filename     = "init.cfg"
    content_type = "text/cloud-config"
    merge_type   = "list(append)+dict(recurse_list)"
    content = templatefile("${path.module}/cloud-init.yml", {
      players  = var.students
      packages = setunion(local.net_tools)
      hostname = "earth-spaceport"
      motd     = file("${path.module}/motd_earth_spaceport")
      ip_addresses = [local.subway_private_ip, local.home_private_ip]
    })
  }

  part {
    filename     = "block_80_and_443"
    content_type = "text/x-shellscript"
    content = file("${path.module}/block_80_and_443")
  }

  part {
    filename     = "disable_ping"
    content_type = "text/x-shellscript"
    content = file("${path.module}/disable_ping")
  }

  part {
    filename     = "ssh_port_666"
    content_type = "text/x-shellscript"
    content = templatefile("${path.module}/change_ssh_port", {
      port: 666
    })
  }

  #part {
  #  filename     = "only_subway"
  #  content_type = "text/x-shellscript"
  #  content = templatefile("${path.module}/only_from", {
  #    ip_addresses: [local.subway_private_ip]
  #  })
  #}
}

#
# On many instances we block all traffic except from one other instance.
# This prevents terraform using home as a bastion to connect to each instance
# to determine if cloud-init succeeded.
#

resource "aws_instance" "earth_spaceport" {
  subnet_id                   = aws_subnet.earth.id
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = "t2.micro"
  private_ip                  = local.earth_spaceport_private_ip
  key_name                    = aws_key_pair.key.key_name
  vpc_security_group_ids      = [
    aws_security_group.allow_all_internal.id,
    aws_security_group.http_egress_to_world.id
  ]

#
# Because we are using locals to store ip's terraform doesnt actually
# properly resolve dependencies. This is why we need depends_on.
#
#
  user_data_base64            = data.template_cloudinit_config.earth_spaceport.rendered

  tags = merge(local.common_tags, { Name = "total_recon/earth_spaceport" })

  connection {
    bastion_host        = aws_instance.home.public_ip
    bastion_port        = 22
    host                = self.private_ip
    port                = 666
    user                = "ubuntu"
    private_key         = tls_private_key.key.private_key_pem
  }
  provisioner "file" {
    source = "${path.module}/ttylog"
    destination = "/home/ubuntu/recon"
  }
  provisioner "file" {
    source = "${path.module}/tty_setup"
    destination = "/home/ubuntu/recon/tty_setup"
  }
  provisioner "file" {
    source = "${path.module}/only_from"
    destination = "/home/ubuntu/recon/only_from"
  }
  provisioner "remote-exec" {
    inline = [
      "cloud-init status --wait --long",
      "cd /home/ubuntu/recon",
      "sudo chmod +x tty_setup",
      "sudo chmod +x only_from",
      "sudo ./only_from",
      "sudo ./tty_setup",
      "rm -rf /home/ubuntu/recon"
    ]
  }
}

data "template_cloudinit_config" "mars_spaceport" {
  gzip          = true
  base64_encode = true

  part {
    filename     = "bash_history.cfg"
    content_type = "text/cloud-config"
    merge_type   = "list(append)+dict(recurse_list)"
    content = templatefile("${path.module}/bash_history.yml.tpl", {
      aws_key_id  = var.aws_access_key_id
      aws_sec_key = var.aws_secret_access_key
      scenario_id = var.scenario_id
      players     = var.students
    })
  }

  part {
    filename     = "init.cfg"
    content_type = "text/cloud-config"
    merge_type   = "list(append)+dict(recurse_list)"
    content = templatefile("${path.module}/cloud-init.yml", {
      players  = var.students
      packages = setunion(local.net_tools)
      hostname = "mars-spaceport"
      motd     = file("${path.module}/motd_mars_spaceport")
      ip_addresses = [local.earth_spaceport_private_ip, local.home_private_ip]
    })
  }
}

resource "aws_instance" "mars_spaceport" {
  subnet_id                   = aws_subnet.mars.id
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = "t2.micro"
  private_ip                  = local.mars_spaceport_private_ip
  key_name                    = aws_key_pair.key.key_name
  vpc_security_group_ids      = [
    aws_security_group.allow_all_internal.id,
    aws_security_group.http_egress_to_world.id
  ]

  user_data_base64            = data.template_cloudinit_config.mars_spaceport.rendered

  tags = merge(local.common_tags, { Name = "total_recon/mars_spaceport" })
  connection {
    bastion_host        = aws_instance.home.public_ip
    bastion_port        = 22
    host                = self.private_ip
    port                = 22
    user                = "ubuntu"
    private_key         = tls_private_key.key.private_key_pem
  }
  provisioner "file" {
    source = "${path.module}/ttylog"
    destination = "/home/ubuntu/recon"
  }
  provisioner "file" {
    source = "${path.module}/tty_setup"
    destination = "/home/ubuntu/recon/tty_setup"
  }
  provisioner "file" {
    source = "${path.module}/only_from"
    destination = "/home/ubuntu/recon/only_from"
  }
  provisioner "remote-exec" {
    inline = [
      "cloud-init status --wait --long",
      "cd /home/ubuntu/recon",
      "sudo chmod +x tty_setup",
      "sudo ./tty_setup",
      "sudo chmod +x only_from",
      "sudo ./only_from",
      "rm -rf /home/ubuntu/recon"
    ]
  }
}


data "template_cloudinit_config" "venusville" {
  gzip          = true
  base64_encode = true

  part {
    filename     = "bash_history.cfg"
    content_type = "text/cloud-config"
    merge_type   = "list(append)+dict(recurse_list)"
    content = templatefile("${path.module}/bash_history.yml.tpl", {
      aws_key_id  = var.aws_access_key_id
      aws_sec_key = var.aws_secret_access_key
      scenario_id = var.scenario_id
      players     = var.students
    })
  }

  part {
    filename     = "init.cfg"
    content_type = "text/cloud-config"
    merge_type   = "list(append)+dict(recurse_list)"
    content = templatefile("${path.module}/cloud-init.yml", {
      players  = var.students
      packages = setunion(local.net_tools, ["bind9", "apache2"])
      hostname = "venusville"
      motd     = file("${path.module}/motd_venusville")
      ip_addresses = [local.mars_spaceport_private_ip, local.home_private_ip]
    })
  }

  part {
    filename     = "ssh_port_123"
    content_type = "text/x-shellscript"
    content = templatefile("${path.module}/change_ssh_port", {
      port: 123
    })
  }
}

resource "aws_instance" "venusville" {
  subnet_id                   = aws_subnet.mars.id
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = "t2.micro"
  private_ip                  = local.venusville_private_ip
  key_name                    = aws_key_pair.key.key_name
  vpc_security_group_ids      = [
    aws_security_group.allow_all_internal.id,
    aws_security_group.http_egress_to_world.id
  ]

  user_data_base64            = data.template_cloudinit_config.venusville.rendered

  tags = merge(local.common_tags, { Name = "total_recon/venusville" })
  connection {
    bastion_host        = aws_instance.home.public_ip
    bastion_port        = 22
    host                = self.private_ip
    port                = 123
    user                = "ubuntu"
    private_key         = tls_private_key.key.private_key_pem
  }
  provisioner "file" {
    source = "${path.module}/ttylog"
    destination = "/home/ubuntu/recon"
  }
  provisioner "file" {
    source = "${path.module}/tty_setup"
    destination = "/home/ubuntu/recon/tty_setup"
  }
  provisioner "file" {
    source = "${path.module}/only_from"
    destination = "/home/ubuntu/recon/only_from"
  }
  provisioner "remote-exec" {
    inline = [
      "cloud-init status --wait --long",
      "cd /home/ubuntu/recon",
      "sudo chmod +x tty_setup",
      "sudo chmod +x only_from",
      "sudo ./only_from",
      "sudo ./tty_setup",
      "rm -rf /home/ubuntu/recon"
    ]
  }
}

data "template_cloudinit_config" "last_resort" {
  gzip          = true
  base64_encode = true

  part {
    filename     = "bash_history.cfg"
    content_type = "text/cloud-config"
    merge_type   = "list(append)+dict(recurse_list)"
    content = templatefile("${path.module}/bash_history.yml.tpl", {
      aws_key_id  = var.aws_access_key_id
      aws_sec_key = var.aws_secret_access_key
      scenario_id = var.scenario_id
      players     = var.students
    })
  }

  part {
    filename     = "init.cfg"
    content_type = "text/cloud-config"
    merge_type   = "list(append)+dict(recurse_list)"
    content = templatefile("${path.module}/cloud-init.yml", {
      players  = var.students
      packages = []
      hostname = "last-resort"
      ip_addresses = [local.venusville_private_ip, local.home_private_ip]
      motd     = file("${path.module}/motd_last_resort")
    })
  }

  part {
    filename     = "ssh_port_2345"
    content_type = "text/x-shellscript"
    content = templatefile("${path.module}/change_ssh_port", {
      port: 2345
    })
  }
}

resource "aws_instance" "last_resort" {
  subnet_id                   = aws_subnet.mars.id
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = "t2.micro"
  private_ip                  = local.last_resort_private_ip
  key_name                    = aws_key_pair.key.key_name
  vpc_security_group_ids      = [
    aws_security_group.allow_all_internal.id,
    aws_security_group.http_egress_to_world.id
  ]

  user_data_base64            = data.template_cloudinit_config.last_resort.rendered

  tags = merge(local.common_tags, { Name = "total_recon/last_resort" })
  connection {
    bastion_host        = aws_instance.home.public_ip
    bastion_port        = 22
    host                = self.private_ip
    port                = 2345
    user                = "ubuntu"
    private_key         = tls_private_key.key.private_key_pem
  }
  provisioner "file" {
    source = "${path.module}/ttylog"
    destination = "/home/ubuntu/recon"
  }
  provisioner "file" {
    source = "${path.module}/tty_setup"
    destination = "/home/ubuntu/recon/tty_setup"
  }
  provisioner "file" {
    source = "${path.module}/only_from"
    destination = "/home/ubuntu/recon/only_from"
  }
  provisioner "remote-exec" {
    inline = [
      "cloud-init status --wait --long",
      "cd /home/ubuntu/recon",
      "sudo chmod +x tty_setup",
      "sudo ./tty_setup",
      "sudo chmod +x only_from",
      "sudo ./only_from",
      "rm -rf /home/ubuntu/recon"
    ]
  }
}


data "template_cloudinit_config" "resistance_base" {
  gzip          = true
  base64_encode = true

  part {
    filename     = "bash_history.cfg"
    content_type = "text/cloud-config"
    merge_type   = "list(append)+dict(recurse_list)"
    content = templatefile("${path.module}/bash_history.yml.tpl", {
      aws_key_id  = var.aws_access_key_id
      aws_sec_key = var.aws_secret_access_key
      scenario_id = var.scenario_id
      players     = var.students
    })
  }

  part {
    filename     = "init.cfg"
    content_type = "text/cloud-config"
    merge_type   = "list(append)+dict(recurse_list)"
    content = templatefile("${path.module}/cloud-init.yml", {
      players  = var.students
      packages = local.net_tools
      hostname = "resistance-base"
      motd     = templatefile("${path.module}/motd_resistance_base",{
        resistance_base_private_ip = local.resistance_base_private_ip
        })
      ip_addresses = [local.subway_private_ip,
                      local.earth_spaceport_private_ip,
                      local.mars_spaceport_private_ip,
                      local.venusville_private_ip]
    })
  }

  part {
    filename     = "ssh_port_632"
    content_type = "text/x-shellscript"
    content = templatefile("${path.module}/change_ssh_port", {
      port: 632
    })
  }

  part {
    filename     = "nmap_to_sudoers"
    content_type = "text/x-shellscript"
    content = templatefile("${path.module}/nmap_to_sudoers", {
      players: var.students
    })
  }

}

resource "aws_instance" "resistance_base" {
  subnet_id                   = aws_subnet.mars.id
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = "t2.micro"
  private_ip                  = local.resistance_base_private_ip
  key_name                    = aws_key_pair.key.key_name
  vpc_security_group_ids      = [
    aws_security_group.allow_all_internal.id,
    aws_security_group.http_egress_to_world.id
  ]
  user_data_base64            = data.template_cloudinit_config.resistance_base.rendered

  tags = merge(local.common_tags, { Name = "total_recon/resistance_base" })
  connection {
    bastion_host        = aws_instance.home.public_ip
    bastion_port        = 22
    host                = self.private_ip
    port                = 632
    user                = "ubuntu"
    private_key         = tls_private_key.key.private_key_pem
  }
  provisioner "file" {
    source = "${path.module}/ttylog"
    destination = "/home/ubuntu/recon"
  }
  provisioner "file" {
    source = "${path.module}/tty_setup"
    destination = "/home/ubuntu/recon/tty_setup"
  }
  provisioner "file" {
    source = "${path.module}/drop_all_from"
    destination = "/home/ubuntu/recon/drop_all_from"
  }
  provisioner "remote-exec" {
    inline = [
      "cloud-init status --wait --long",
      "cd /home/ubuntu/recon",
      "sudo chmod +x tty_setup",
      "sudo ./tty_setup",
      "sudo chmod +x drop_all_from",
      "sudo ./drop_all_from",
      "rm -rf /home/ubuntu/recon"
    ]
  }
}

data "template_cloudinit_config" "stealth_xmas" {
  gzip          = true
  base64_encode = true
  
  part {
    filename     = "disable_ping"
    content_type = "text/x-shellscript"
    content = file("${path.module}/disable_ping")
  }

  part {
    filename     = "block_all_but_xmas"
    content_type = "text/x-shellscript"
    content = file("${path.module}/block_all_but_xmas")
  }

  part {
    filename     = "ssh_port_444"
    content_type = "text/x-shellscript"
    content = templatefile("${path.module}/change_ssh_port", {
      port: 444
    })
  }
}

resource "aws_instance" "stealth_xmas" {
  subnet_id                   = aws_subnet.mars.id
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = "t2.nano"
  private_ip                  = "10.0.233.34"
  key_name                    = aws_key_pair.key.key_name
  vpc_security_group_ids      = [
    aws_security_group.allow_all_internal.id,
    aws_security_group.http_egress_to_world.id
  ]
  user_data_base64            = data.template_cloudinit_config.stealth_xmas.rendered

  tags = merge(local.common_tags, { Name = "total_recon/stealth_xmas" })
  connection {
    bastion_host        = aws_instance.home.public_ip
    bastion_port        = 22
    host                = self.private_ip
    port                = 444
    user                = "ubuntu"
    private_key         = tls_private_key.key.private_key_pem
  }
  provisioner "file" {
    source = "${path.module}/ttylog"
    destination = "/home/ubuntu/recon"
  }
  provisioner "file" {
    source = "${path.module}/tty_setup"
    destination = "/home/ubuntu/recon/tty_setup"
  }
  provisioner "remote-exec" {
    inline = [
      "cloud-init status --wait --long",
      "cd /home/ubuntu/recon",
      "sudo chmod +x tty_setup",
      "sudo ./tty_setup",
      "rm -rf /home/ubuntu/recon"
    ]
  }
}

data "template_cloudinit_config" "stealth_null" {
  gzip          = true
  base64_encode = true

  part {
    filename     = "disable_ping"
    content_type = "text/x-shellscript"
    content = file("${path.module}/disable_ping")
  }

  part {
    filename     = "block_all_but_null"
    content_type = "text/x-shellscript"
    content = file("${path.module}/block_all_but_null")
  }
}

resource "aws_instance" "stealth_null" {
  subnet_id                   = aws_subnet.mars.id
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = "t2.nano"
  private_ip                  = "10.0.233.36"
  key_name                    = aws_key_pair.key.key_name
  vpc_security_group_ids      = [
    aws_security_group.allow_all_internal.id,
    aws_security_group.http_egress_to_world.id
  ]
  user_data_base64            = data.template_cloudinit_config.stealth_null.rendered

  tags = merge(local.common_tags, { Name = "total_recon/stealth_null" })
  connection {
    bastion_host        = aws_instance.home.public_ip
    bastion_port        = 22
    host                = self.private_ip
    port                = 22
    user                = "ubuntu"
    private_key         = tls_private_key.key.private_key_pem
  }
  provisioner "file" {
    source = "${path.module}/ttylog"
    destination = "/home/ubuntu/recon"
  }
  provisioner "file" {
    source = "${path.module}/tty_setup"
    destination = "/home/ubuntu/recon/tty_setup"
  }
  provisioner "remote-exec" {
    inline = [
      "cloud-init status --wait --long",
      "cd /home/ubuntu/recon",
      "sudo chmod +x tty_setup",
      "sudo ./tty_setup",
      "rm -rf /home/ubuntu/recon"
    ]
  }
}

data "template_cloudinit_config" "stealth_fin" {
  gzip          = true
  base64_encode = true

  part {
    filename     = "disable_ping"
    content_type = "text/x-shellscript"
    content = file("${path.module}/disable_ping")
  }

  part {
    filename     = "block_all_but_fin"
    content_type = "text/x-shellscript"
    content = file("${path.module}/block_all_but_fin")
  }
}

resource "aws_instance" "stealth_fin" {
  subnet_id                   = aws_subnet.mars.id
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = "t2.nano"
  private_ip                  = "10.0.233.38"
  key_name                    = aws_key_pair.key.key_name
  vpc_security_group_ids      = [
    aws_security_group.allow_all_internal.id,
    aws_security_group.http_egress_to_world.id
  ]
  user_data_base64            = data.template_cloudinit_config.stealth_fin.rendered

  tags = merge(local.common_tags, { Name = "total_recon/stealth_null" })
  connection {
    bastion_host        = aws_instance.home.public_ip
    bastion_port        = 22
    host                = self.private_ip
    port                = 22
    user                = "ubuntu"
    private_key         = tls_private_key.key.private_key_pem
  }
  provisioner "file" {
    source = "${path.module}/ttylog"
    destination = "/home/ubuntu/recon"
  }
  provisioner "file" {
    source = "${path.module}/tty_setup"
    destination = "/home/ubuntu/recon/tty_setup"
  }
  provisioner "remote-exec" {
    inline = [
      "cloud-init status --wait --long",
      "cd /home/ubuntu/recon",
      "sudo chmod +x tty_setup",
      "sudo ./tty_setup",
      "rm -rf /home/ubuntu/recon"
    ]
  }
}

data "template_cloudinit_config" "control_room" {
  gzip          = true
  base64_encode = true
  
  part {
    filename     = "bash_history.cfg"
    content_type = "text/cloud-config"
    merge_type   = "list(append)+dict(recurse_list)"
    content = templatefile("${path.module}/bash_history.yml.tpl", {
      aws_key_id  = var.aws_access_key_id
      aws_sec_key = var.aws_secret_access_key
      scenario_id = var.scenario_id
      players     = var.students
    })
  }

  part {
    filename     = "init.cfg"
    content_type = "text/cloud-config"
    merge_type   = "list(append)+dict(recurse_list)"
    content = templatefile("${path.module}/cloud-init.yml", {
      players  = var.students
      packages = local.net_tools
      hostname = "control-room"
      motd     = file("${path.module}/motd_control_room")
      ip_addresses = [local.subway_private_ip,
                      local.earth_spaceport_private_ip,
                      local.mars_spaceport_private_ip,
                      local.venusville_private_ip]
    })
  }

  part {
    filename     = "ssh_port_1938"
    content_type = "text/x-shellscript"
    content = templatefile("${path.module}/change_ssh_port", {
      port: 1938
    })
  }

  part {
    filename     = "fake_ports"
    content_type = "text/x-shellscript"
    content = templatefile("${path.module}/control_fake_ports", {
      ports = [103, 233, 409, 666, 1783, 3333, 1509, 2010]
    })
  }

   part {
    filename     = "nmap_to_sudoers"
    content_type = "text/x-shellscript"
    content = templatefile("${path.module}/nmap_to_sudoers", {
      players: var.students
    })
  }
  
}

resource "aws_instance" "control_room" {
  subnet_id                   = aws_subnet.mars.id
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = "t2.micro"
  private_ip                  = "10.0.250.5"
  key_name                    = aws_key_pair.key.key_name
  vpc_security_group_ids      = [
    aws_security_group.allow_all_internal.id,
    aws_security_group.http_egress_to_world.id
  ]
  user_data_base64            = data.template_cloudinit_config.control_room.rendered

  tags = merge(local.common_tags, { Name = "total_recon/control_room" })
  connection {
    bastion_host        = aws_instance.home.public_ip
    bastion_port        = 22
    host                = self.private_ip
    port                = 1938
    user                = "ubuntu"
    private_key         = tls_private_key.key.private_key_pem
  }

  provisioner "file" {
    source = "${path.module}/drop_all_from"
    destination = "/home/ubuntu//drop_all_from"
  }
  provisioner "file" {
    source = "${path.module}/reactor_control"
    destination = "/home/ubuntu/reactor_control"
  }
  provisioner "file" {
    source = "${path.module}/control_script"
    destination = "/home/ubuntu/control_script"
  }
  provisioner "file" {
    source = "${path.module}/crontab_entry"
    destination = "/home/ubuntu/crontab_entry"
  }
  provisioner "file" {
    source = "${path.module}/usernames_and_connection"
    destination = "/home/ubuntu/users_and_conns"
  }
  provisioner "file" {
    source = "${path.module}/check_reactors.sh"
    destination = "/home/ubuntu/check_reactors.sh"
  }
  provisioner "remote-exec" {
    inline = [
      "cloud-init status --wait --long",
      "sudo hostname control-room",
      "cd /home/ubuntu",
      "sudo mkdir recon",
      "sudo mv control_script recon/control_script",
      "sudo chmod +x users_and_conns",
      "sudo ./users_and_conns",
      "sudo crontab crontab_entry",
      "sudo chmod +x /home/ubuntu/check_reactors.sh",
      "sudo chmod +x reactor_control",
      "sudo ./reactor_control",
      "sudo chmod +x drop_all_from",
      "sudo ./drop_all_from",
      "sudo mkdir /look-in-here",
      "sudo mv /bin/chmod /look-in-here/chmod",
      "rm users_and_conns",
      "rm crontab_entry",
      "rm reactor_control",
      "rm drop_all_from",
      "sudo rm -rf recon"
    ]
  }
}
