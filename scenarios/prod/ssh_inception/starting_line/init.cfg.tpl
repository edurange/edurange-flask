#cloud-config
repo_update: true
repo_upgrade: all
ssh_pwauth: yes
hostname: starting-line
packages:
- nmap
- iputils-ping
- net-tools
- ftp
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
  content: |2
       _____ _             _   _               _      _
      / ____| |           | | (_)             | |    (_)
     | (___ | |_ __ _ _ __| |_ _ _ __   __ _  | |     _ _ __   ___
      \___ \| __/ _  |  __| __| |  _ \ / _  | | |    | |  _ \ / _ \
      ____) | || (_| | |  | |_| | | | | (_| | | |____| | | | |  __/
     |_____/ \__\__,_|_|   \__|_|_| |_|\__, | |______|_|_| |_|\___|
                                        __/ |
                                       |___/

    "It's a week the first level down. Six months the second level
    down, and... the third level..."

    Go a level deeper. You will find the next host at 10.0.0.7.
    The trick is that the ssh port has been changed to 123. Good luck!

    Helpful commands: ssh, help, man
runcmd:
- chmod -x /etc/update-motd.d/*
- rm /etc/legal
- hostname starting-line
- service sshd reload
%{ for player in players ~}
- echo ${player.variables.secret_starting_line} > /home/${player.login}/secret
%{ endfor ~}
