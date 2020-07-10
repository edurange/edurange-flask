#cloud-config
repo_update: true
repo_upgrade: all
hostname: anon-ftp
packages:
- vsftpd
users:
- default
write_files:
- path: /etc/vsftpd.conf
  encoding: b64
  content: ${base64encode(vsftpd_conf)}
- path: /var/ftp/hint
  encoding: b64
  permissions: '0444'
  content: ${base64encode(hint)}
runcmd:
- sudo hostname anon-ftp
- service vsftpd restart
