# The "interface" with edurange-server is defined by variables and outputs.
variable "students" {
  type = list(object({
    login              = string,
    password           = object({ plaintext = string, hash = string }),
  }))
  description = "list of players in students group"
  
  default = []
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

variable "scenario_id" {
  type        = string
  description = "identifier for instance of this scenario"
}

variable "env" {
  type        = string
  description = "For example testing/development/production"
  default     = "development"
}

variable "owner" {
  type        = string
  default     = "unknown"
}

output "instances" {
  value = [{
    name = "strace"
    ip_address_public  = aws_instance.strace.public_ip
    ip_address_private = aws_instance.strace.private_ip
  }]
}

# To be a good citizen scenario authors should tag all resources with these
# common tags and a Name tag.

locals {
  common_tags = {
    scenario_id = var.scenario_id
    env         = var.env
    owner       = var.owner
  }
}

provider "local" {
  version    = "~> 1"
}

provider "template" {
  version = "~> 2"
}

provider "tls" {
  version = "~> 2"
}

provider "aws" {
  version    = "~> 2"
  profile    = "default"
  region     = var.aws_region
  access_key = var.aws_access_key_id
  secret_key = var.aws_secret_access_key
}

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

# save the private key locally for debugging
resource "local_file" "id_rsa" {
  sensitive_content  = tls_private_key.key.private_key_pem
  filename           = "${path.cwd}/id_rsa"
  provisioner "local-exec" {
    command = "chmod 600 ${path.cwd}/id_rsa"
  }
}

# upload the public key to aws
resource "aws_key_pair" "key" {
  key_name   = "strace/${var.scenario_id}"
  public_key = tls_private_key.key.public_key_openssh
}


data "template_cloudinit_config" "strace" {
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
    content = templatefile("${path.module}/cloud-init.yml.tpl", {
      players  = var.students
      motd     = file("${path.module}/motd")
      packages = ["gdb", "build-essential", "colordiff", "strace"]
      hostname = "strace"
    })
  }
}

resource "aws_vpc" "cloud" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name 	= "strace/cloud"
    scenario_id = var.scenario_id
  }
}

resource "aws_internet_gateway" "default"{
  vpc_id = aws_vpc.cloud.id
}

resource "aws_subnet" "public" {
  vpc_id 	= aws_vpc.cloud.id
  cidr_block    = "10.0.0.0/24"
  tags = {
    Name = "strace/public"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.cloud.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.default.id
  }

}

resource "aws_route_table_association" "strace_subnut_route_table_association"{
  subnet_id 	 = aws_subnet.public.id
  route_table_id = aws_route_table.public.id 
}

resource "aws_security_group" "ssh_in_http_out" {
  vpc_id = aws_vpc.cloud.id
  name = "strace/${var.scenario_id}"
  
  ingress {
    from_port   = "22"
    to_port     = "22"
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = "443"
    to_port     = "443"
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = "80"
    to_port     = "80"
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

}

resource "aws_instance" "strace" {
  ami                    	 = data.aws_ami.ubuntu.id
  instance_type          	 = "t2.nano"
  private_ip 		 	 = "10.0.0.5"
  associate_public_ip_address    = true
  source_dest_check 		 = false
  subnet_id 		 	 = aws_subnet.public.id
  user_data_base64       	 = data.template_cloudinit_config.strace.rendered
  key_name               	 = aws_key_pair.key.key_name
  vpc_security_group_ids 	 = [aws_security_group.ssh_in_http_out.id]
  

  tags = merge(local.common_tags, {
    Name = "strace"
  })

  connection {
    host        = self.public_ip
    type        = "ssh"
    user        = "ubuntu"
    private_key = tls_private_key.key.private_key_pem
  }

  provisioner "file" {
    source = "${path.module}/files"
    destination = "/home/ubuntu/strace"
  }

  provisioner "file" {
    content = templatefile("${path.module}/install", {
      players = var.students
    })
    destination = "/home/ubuntu/strace/install"
  }

  provisioner "file" {
    source = "${path.module}/ttylog"
    destination = "/home/ubuntu/strace"
  }

  provisioner "file" {
    source = "${path.module}/tty_setup"
    destination = "/home/ubuntu/strace/tty_setup"
  }

  provisioner "remote-exec" {
    inline = [
      "set -eux",
      "cloud-init status --wait --long",
      "cd /home/ubuntu/strace",
      "chmod +x install",
      "chmod +x tty_setup",
      "sudo ./tty_setup",
      "sudo ./install",
      "rm -rf /home/ubuntu/strace"
    ]
  }

}
