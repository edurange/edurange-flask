#cloud-config
repo_update: true
repo_upgrade: all
ssh_pwauth: yes
hostname: first-stop
packages:
- nmap
- iputils-ping
- net-tools
- ftp
- ipcalc
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
runcmd:
- rm /etc/update-motd.d/*
- rm /etc/legal
- hostname first-stop
- sed -i '/Port/s/^.*$/Port 123/' /etc/ssh/sshd_config
- service sshd restart
%{ for player in players ~}
- echo ${player.variables.secret_first_stop} > /home/${player.login}/secret
%{ endfor ~}
