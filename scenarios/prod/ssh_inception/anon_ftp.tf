resource "aws_instance" "anon_ftp" {
  ami           = data.aws_ami.ubuntu.id
  instance_type = "t2.nano"
  private_ip    = "10.0.0.14"
  subnet_id     = aws_subnet.private.id
  depends_on    = [aws_instance.nat]
  key_name      = aws_key_pair.key.key_name
  user_data = templatefile("${path.module}/anon_ftp/init.cfg.tpl", {
    hint = templatefile("${path.module}/anon_ftp/hint.tpl", {
      fifth_stop_password_key = random_string.fifth_stop_password_key.result
    })
    vsftpd_conf = file("${path.module}/anon_ftp/vsftpd.conf")
  })
  vpc_security_group_ids = [aws_security_group.private.id]
  tags = merge(local.common_tags, {
    Name = "ssh_inception/anon_ftp"
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

  provisioner "remote-exec" {
    inline = [
      "cloud-init status --wait --long",
      "sudo service sshd stop"
    ]
  }
}
