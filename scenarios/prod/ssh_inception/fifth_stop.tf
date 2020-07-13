data "template_cloudinit_config" "fifth_stop" {
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
    content = templatefile("${path.module}/fifth_stop/init.cfg.tpl", {
      players = var.students
      module_path = path.module
    })
  }
}

resource "aws_instance" "fifth_stop" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = "t2.small"
  private_ip             = "10.0.0.17"
  subnet_id              = aws_subnet.private.id
  depends_on             = [aws_instance.nat]
  key_name               = aws_key_pair.key.key_name
  user_data_base64       = data.template_cloudinit_config.fifth_stop.rendered
  vpc_security_group_ids = [aws_security_group.private.id]
  tags = merge(local.common_tags, {
    Name = "ssh_inception/fifth_stop"
  })
  connection {
    host        = coalesce(self.public_ip, self.private_ip)
    type        = "ssh"
    user        = "ubuntu"
    private_key = tls_private_key.key.private_key_pem

    # connect to NAT first, then connect to host
    bastion_user        = "ec2-user"
    bastion_host        = aws_instance.nat.public_ip
    bastion_private_key = tls_private_key.key.private_key_pem
  }

  provisioner "file" {
    source = "${path.module}/ttylog"
    destination = "/home/ubuntu"
  }

  provisioner "file" {
    source = "${path.module}/tty_setup"
    destination = "/home/ubuntu/tty_setup"
  }

  provisioner "file" {
    source = "${path.module}/clear_logs"
    destination = "/home/ubuntu/clear_logs"
  }

  provisioner "remote-exec" {
    inline = [
      "set -eux",
      "cloud-init status --wait --long",
      "chmod +x /home/ubuntu/tty_setup",
      "chmod +x /home/ubuntu/clear_logs",
      "sudo mv /home/ubuntu/clear_logs /usr/bin/clear_logs",
      "sudo /home/ubuntu/tty_setup"
    ]
  }
}
