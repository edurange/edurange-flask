data "template_cloudinit_config" "satans_palace" {
  gzip          = true
  base64_encode = true

  part {
    filename     = "init.cfg"
    content_type = "text/cloud-config"
    content = templatefile("${path.module}/satans_palace/init.cfg.tpl", {
      players = var.students
      motd    = file("${path.module}/satans_palace/motd")
      setup_player_home = file("${path.module}/satans_palace/setup_player_home")
    })
  }
}

resource "aws_instance" "satans_palace" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = "t2.nano"
  private_ip             = "10.0.0.19"
  subnet_id              = aws_subnet.private.id
  depends_on             = [aws_instance.nat]
  key_name               = aws_key_pair.key.key_name
  user_data_base64       = data.template_cloudinit_config.satans_palace.rendered
  vpc_security_group_ids = [aws_security_group.private.id]
  tags = merge(local.common_tags, {
    Name = "ssh_inception/satans_palace"
  })
  connection {
    host        = self.private_ip
    port        = 666
    type        = "ssh"
    user        = "ubuntu"
    private_key = tls_private_key.key.private_key_pem

    # connect to NAT first, then connect to host
    bastion_user        = "ec2-user"
    bastion_host        = aws_instance.nat.public_ip
    bastion_port        = 22
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

  provisioner "remote-exec" {
    inline = [
      "set -eux",
      "cloud-init status --wait --long",
      "chmod +x /home/ubuntu/tty_setup",
      "sudo /home/ubuntu/tty_setup"
    ]
  }
}
