#cloud-config (basis)
repo_update: true
repo_upgrade: all
ssh_pwauth: yes
hostname: ${hostname}
users:
- default
%{ for player in players ~}
- name: ${player.login}
  passwd: ${player.password.hash}
  lock_passwd: false
  shell: /bin/bash
%{ endfor ~}
write_files:
- path: /etc/motd
  encoding: b64
  content: ${base64encode(motd)}
runcmd:
- set -eu
- chmod -x /etc/update-motd.d/*
- rm /etc/legal
- hostname ${hostname}
- service ssh restart
