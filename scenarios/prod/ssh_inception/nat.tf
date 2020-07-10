data "template_cloudinit_config" "nat" {
  gzip          = true
  base64_encode = true

  part {
    filename     = "init.cfg"
    content_type = "text/cloud-config"
    content = templatefile("${path.module}/nat/init.cfg.tpl", {
      players = var.students
    })
  }
}

resource "aws_instance" "nat" {
  ami                         = data.aws_ami.nat.id
  instance_type               = "t2.small"
  private_ip                  = "10.0.129.5"
  subnet_id                   = aws_subnet.public.id
  vpc_security_group_ids      = [aws_security_group.public.id]
  associate_public_ip_address = true
  source_dest_check           = false
  user_data_base64            = data.template_cloudinit_config.nat.rendered
  key_name                    = aws_key_pair.key.key_name
  tags = merge(local.common_tags, {
    Name = "ssh_inception/nat"
  })
  connection {
    host        = aws_instance.nat.public_ip
    port        = 22
    type        = "ssh"
    user        = "ec2-user"
    private_key = tls_private_key.key.private_key_pem
  }

  provisioner "file" {
    source = "${path.module}/nat/motd"
    destination = "/tmp/message"
  }

  provisioner "remote-exec" {
    inline = [      
      "for homedir in /home/*; do sudo cp /tmp/message $homedir; done",
      "sudo chmod 666 /etc/motd",
      "sudo cat /tmp/message > /etc/motd"
    ]
  }
}
