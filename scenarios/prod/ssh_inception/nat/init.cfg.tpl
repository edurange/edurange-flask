#cloud-config
repo_update: true
repo_upgrade: all
ssh_pwauth: yes
hostname: nat
preserve_hostname: false
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
runcmd:
- hostname nat
- service sshd restart
