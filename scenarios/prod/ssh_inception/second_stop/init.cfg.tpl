#cloud-config
repo_update: true
repo_upgrade: all
ssh_pwauth: yes
hostname: second-stop
packages:
- nmap
- iputils-ping
- net-tools
- ftp
users:
- default
%{ for player in players ~}
- name: ${player.login}
  lock_passwd: false
  passwd: ${player.password.hash}
  shell: /bin/bash
%{ endfor ~}
write_files:
- path: /etc/motd
  encoding: b64
  content: ${base64encode(motd)}
- path: /root/id_rsa
  encoding: b64
  permissions: '0444'
  content: ${base64encode(ssh_private_key)}
runcmd:
- sudo rm /etc/update-motd.d/*
- sudo rm /etc/legal
- sudo hostname second-stop
%{ for player in players ~}
- ln /root/id_rsa /home/${player.login}/id_rsa
- echo ${player.variables.secret_second_stop} > /home/${player.login}/secret
%{ endfor ~}
- service sshd reload
