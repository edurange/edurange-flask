#cloud-config
repo_update: true
repo_upgrade: all
ssh_pwauth: yes
hostname: fifth-stop
packages:
- nmap
- iputils-ping
- net-tools
- ftp
users:
- default
%{ for player in players ~}
- name: ${player.login}
  passwd: ${player.variables.fifth_stop_password.hash}
  lock_passwd: false
  shell: /bin/bash
%{ endfor ~}
write_files:
- path: /etc/motd
  encoding: b64
  content: ${filebase64("${module_path}/fifth_stop/motd")}
- path: /root/setup_player_home
  encoding: b64
  content: ${filebase64("${module_path}/fifth_stop/setup_player_home")}
  permissions: '0550'
runcmd:
- rm /etc/update-motd.d/*
- rm /etc/legal
- hostname fifth-stop
- service sshd reload
%{ for player in players ~}
- /root/setup_player_home ${player.login} ${player.variables.satans_palace_password.plaintext}
- echo ${player.variables.secret_fifth_stop} > /home/${player.login}/secret
%{ endfor ~}
