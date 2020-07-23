
#!/bin/sh
#***********************************************************
# This script will open a telnet session to a host using variables for
#    targethost = ip address to do the telnet to
#    username = the username to use for the login attempt
#    ctpassword = the cleartext password
#***********************************************************
echo "Script start."
targethost=10.0.37.6
username=telnet_bot
ctpassword=telnet_is_cool_cba321
cmd_to_execute=exit
( echo open ${targethost}
sleep 1
echo ${username}
sleep 5
echo ${ctpassword}
sleep 5
echo ${cmd1}
sleep 2
 ) | telnet
 echo "Script end."

