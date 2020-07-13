#cloud-config
repo_update: true
repo_upgrade: all
ssh_pwauth: yes
hostname: satans-palace
users:
- default
%{ for player in players ~}
- name: ${player.login}
  passwd: ${player.variables.satans_palace_password.hash}
  lock_passwd: false
  shell: /bin/bash
%{ endfor ~}
write_files:
- path: /etc/motd
  encoding: b64
  content: ${base64encode(motd)}
- path: /root/setup_player_home
  encoding: b64
  content: ${base64encode(setup_player_home)}
  permissions: '0550'
runcmd:
- rm /etc/update-motd.d/*
- rm /etc/legal
- hostname satans-palace
- sed -i -e '/^\#Port/s/^.*$/Port 666/' /etc/ssh/sshd_config
%{ for player in players ~}
- ['/root/setup_player_home', '${player.login}', '${player.variables.master_string}']
%{ endfor ~}
- service sshd restart
