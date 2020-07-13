#cloud-config
repo_update: true
repo_upgrade: all
ssh_pwauth: yes
hostname: fourth-stop
packages:
- nmap
- iputils-ping
- net-tools
- ftp
users:
- default
%{ for player in players ~}
- name: ${player.login}
  passwd: ${player.variables.fourth_stop_password.hash}
  lock_passwd: false
  shell: /bin/bash
%{ endfor ~}
write_files:
- path: /etc/motd
  encoding: b64
  content: ${filebase64("${module_path}/fourth_stop/motd")}
- path: /root/setup_player_home
  encoding: b64
  permissions: '0550'
  content: ${filebase64("${module_path}/fourth_stop/setup_player_home")}
- path: /root/decrypt_password
  encoding: b64
  content: ${filebase64("${module_path}/fourth_stop/decrypt_password")}
  permissions: '0555'
runcmd:
- rm /etc/update-motd.d/*
- rm /etc/legal
- hostname fourth-stop
- service sshd reload
%{ for player in players ~}
- /root/setup_player_home ${player.login} ${player.variables.fifth_stop_password.plaintext} ${fifth_stop_password_key}
- echo ${player.variables.secret_fourth_stop} > /home/${player.login}/secret
%{ endfor ~}
# block traffic from ThirdStop. players must find a way around this
- iptables -A INPUT -s 10.0.0.13 -j DROP
