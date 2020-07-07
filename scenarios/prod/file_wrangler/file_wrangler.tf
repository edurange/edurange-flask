variable "students" {
  type = list(object({
    login = string,
    password = object({
      plaintext = string,
      hash      = string
    }),
    variables = object({
      manipulate  = string,
      permissions = string
    })
  }))
  description = "list of players"
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
  description = "For example testing/development/production"
  default     = "development"
}

variable "owner" {
  type    = string
  default = "unknown"
}

variable "scenario_id" {
  type        = string
  description = "identifier for instance of this scenario"
}

output "instances" {
  value = [{
    name               = "file_wrangler"
    ip_address_public  = aws_instance.file_wrangler.public_ip
    ip_address_private = aws_instance.file_wrangler.private_ip
  }]
}

locals {
  common_tags = {
    scenario_id = var.scenario_id
    env         = var.env
    owner       = var.owner
  }
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

provider "aws" {
  version    = "~> 2"
  profile    = "default"
  region     = var.aws_region
  access_key = var.aws_access_key_id
  secret_key = var.aws_secret_access_key
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
  key_name   = "file_wrangler/${var.scenario_id}"
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


data "template_cloudinit_config" "file_wrangler" {
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
      hostname = "file-wrangler"
      motd     = file("${path.module}/motd/message.txt")
    })
  }
}

resource "aws_vpc" "cloud" {
  cidr_block = "10.0.0.0/16"
  tags = {
    Name        = "file_wrangler/cloud"
    scenario_id = var.scenario_id
  }
}

resource "aws_internet_gateway" "default" {
  vpc_id = aws_vpc.cloud.id
}

resource "aws_subnet" "public" {
  vpc_id     = aws_vpc.cloud.id
  cidr_block = "10.0.0.0/24"
  tags = {
    Name = "file_wrangler/public"
  }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.cloud.id

  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.default.id
  }

}

resource "aws_route_table_association" "file_wrangler_subnet_route_table_association" {
  subnet_id      = aws_subnet.public.id
  route_table_id = aws_route_table.public.id
}
resource "aws_security_group" "ssh_in_http_out" {
  vpc_id = aws_vpc.cloud.id
  name   = "file_wrangler/${var.scenario_id}"

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

resource "aws_instance" "file_wrangler" {
  ami                         = data.aws_ami.ubuntu.id
  instance_type               = "t2.micro"
  private_ip                  = "10.0.0.5"
  associate_public_ip_address = true
  source_dest_check           = false
  user_data_base64            = data.template_cloudinit_config.file_wrangler.rendered
  subnet_id                   = aws_subnet.public.id
  key_name                    = aws_key_pair.key.key_name
  vpc_security_group_ids      = [aws_security_group.ssh_in_http_out.id]

  tags = merge(local.common_tags, {
    Name = "file_wrangler"
  })

  connection {
    host        = self.public_ip
    type        = "ssh"
    user        = "ubuntu"
    private_key = tls_private_key.key.private_key_pem
  }

  provisioner "remote-exec" {
    inline = [
      "mkdir /home/ubuntu/file_wrangler"
    ]
  }

  provisioner "file" {
    source      = "${path.module}/files"
    destination = "/home/ubuntu/file_wrangler/files"
  }

  provisioner "file" {
    source      = "${path.module}/setup_player"
    destination = "/home/ubuntu/file_wrangler/setup_player"
  }

  provisioner "file" {
    content = templatefile("${path.module}/setup", {
      players = var.students
    })
    destination = "/home/ubuntu/file_wrangler/setup"
  }

  provisioner "file" {
    source      = "${path.module}/python"
    destination = "/home/ubuntu/file_wrangler"
  }

  provisioner "file" {
    source      = "${path.module}/ttylog"
    destination = "/home/ubuntu/file_wrangler"
  }

  provisioner "file" {
    source      = "${path.module}/tty_setup"
    destination = "/home/ubuntu/file_wrangler/tty_setup"
  }

  provisioner "file" {
    source      = "${path.module}/iamfrustrated"
    destination = "/home/ubuntu/file_wrangler/iamfrustrated"
  }

  provisioner "file" {
    source      = "${path.module}/clear_logs"
    destination = "/home/ubuntu/file_wrangler/clear_logs"
  }

  provisioner "remote-exec" {
    inline = [
      "set -eux",
      "cloud-init status --wait --long",
      "chmod +x /home/ubuntu/file_wrangler/setup",
      "chmod +x /home/ubuntu/file_wrangler/setup_player",
      "chmod +x /home/ubuntu/file_wrangler/tty_setup",
      "sudo /home/ubuntu/file_wrangler/tty_setup",
      "chmod +x /home/ubuntu/file_wrangler/iamfrustrated",
      "chmod +x /home/ubuntu/file_wrangler/clear_logs",
      "sudo cp /home/ubuntu/file_wrangler/iamfrustrated /usr/bin/",
      "sudo cp /home/ubuntu/file_wrangler/clear_logs /usr/bin/",
      "sudo /home/ubuntu/file_wrangler/setup"
    ]
  }

}
