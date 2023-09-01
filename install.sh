#!/bin/bash

GRN='\033[0;32m'
YLW='\033[1;33m'
NC='\033[0m'
username=$(whoami)
current_directory=$(pwd)
dbpass="passwordfoo"
dbname="namefoo"
flaskUser="Administrator"
flaskPass="flaskpass"
secretKey="not-so-secret"
hostAddress="localhost"
rootPass="change-me"

# Add pip-executables to the path if they aren't already
grep -qxF 'export PATH=$PATH:/home/$(whoami)/.local/bin' ~/.bashrc || echo 'export PATH=$PATH:/home/$(whoami)/.local/bin' >> ~/.bashrc
source ~/.bashrc

echo -e "${GRN}Installing python3-pip, npm, redis-server,  unzip, postgresql, lib-pq-dev, and wget${NC}"

sudo apt update
sudo apt install -y python3-pip npm redis-server unzip wget postgresql libpq-dev
pip3 install -r requirements/prod.txt

pip3 uninstall pyjwt -y
pip3 uninstall flask-jwt-simple -y

pip3 install -r requirements/prod.txt

npm install
mkdir data
mkdir data/tmp
mkdir logs

echo -e "${YLW}\n\n##### The following set of prompts are for network configuration #####${NC}\n\n"
echo -e "We recommend using your LAN (local) IP for most purposes.\n
If you need the edurange server to be accessible outside your LAN, \n  use your WAN IP or a DNS hostname.\n
WAN IPs/DNS hostnames will expose your installation to the entire \n  Internet and may require additional network configuration.\n
Use at your own risk; we offer limited support for external \n  configurations. \n"

echo -e "${GRN}Please select one of the following options for networking configuration:${NC}"
echo -e "  (1) Use your internal ip address (Recommended for Developer Instances)"
echo -e "  (2) Use your public extern ip address (Advanced)"
echo -e "  (3) Enter your public domain name (For production installations"

#Gather potential IP/Address Options:

#wlo1=$(ip -4 addr show wlo1 | grep -oP '(?<=inet\s)\d+(.\d+){3}' 2>/dev/null)
#eth0=$(ip -4 addr show eth0 | grep -oP '(?<=inet\s)\d+(.\d+){3}' 2>/dev/null)
#enp1s0=$(ip -4 addr show enp1s0 | grep -oP '(?<=inet\s)\d+(.\d+){3}' 2>/dev/null)
#wlan0=$(ip -4 addr show wlan0 | grep -oP '(?<=inet\s)\d+(.\d+){3}' 2>/dev/null)

all=$(/sbin/ip -4 -o addr show scope global | awk '{gsub(/\/.*/,"",$4); print $4}')

#echo "($all)"
#echo "($wlo1)"
#echo "($enp1s0)"
#echo "($eth0)"
#echo "($wlan0)"


hostAddress=''

#TODO Regex this
promptnumber=0

external_ip=$(dig @resolver4.opendns.com myip.opendns.com +short)

echo "$hostAddress"

while [ -z "$hostAddress" ]
do 
  #echo "READING PROMPT NUM"
  read promptnumber

  if [ $promptnumber -eq 1 ]; then
    #echo -e "Your ip is one of these \n$all"
    option1=$(echo "$all" | sed "1p;d")
    option2=$(echo "$all" | sed "2p;d")
    echo "  Please select one of the following Local IP Addresses we detected:"
    echo "  (1) $option1"
    echo "  (2) $option2"

    while [ -z "$hostAddress" ]
    do
      read optnumber
      if [ $optnumber -eq 1 ]; then
        hostAddress="$option1"
      elif [ $optnumber -eq 2 ]; then
        hostAddress="$option2"
      fi
    done
    
  elif [ $promptnumber -eq 2 ]; then
    #echo $external_ip
    hostAddress="$external_ip"
    #echo "$hostAddress CHANGED"
  
  elif [ $promptnumber -eq 3 ]; then
    echo "Enter domain name: "
    read hostAddress
    #echo "$hostAddress CHANGED"
  fi
done

#echo "hostAddress changed to: $hostAddress "

#exit

if [ $# -eq 0 ];
then
	echo -e "${YLW}Please enter your database password:${NC}"
	read dbpass
	echo -e "${YLW}Please enter your database name:${NC}"
	read dbname
	echo -e "${YLW}Please enter your Flask (web interface) username:${NC}"
	read flaskUser
	echo -e "${YLW}Please enter your Flask (web interface) password:${NC}"
	read flaskPass
	#echo -e "${YLW}Please enter your external address (Like example.com):${NC}"
	#read hostAddress
	echo -e "${YLW}Please enter your root password for all containers:${NC}"
	read rootPass
	# Generate secret string for cookie encryption
	secretKey=$(cat /dev/urandom | tr -dc '[:alpha:]' | fold -w ${1:-20} | head -n 1)
	cp ./.env.example ./.env
	sed -i "s/namefoo/${dbname}/" .env
	sed -i "s/passwordfoo/${dbpass}/" .env
	sed -i "s/Administrator/${flaskUser}/" .env
	sed -i "s/flaskpass/${flaskPass}/" .env
	sed -i "s/not-so-secret/${secretKey}/" .env
	sed -i "s/localhost/${hostAddress}/" .env
	sed -i "s/change-me/${rootPass}/" .env
  sed -i "s/URL_TO_BE_CHANGED/${hostAddress}/" edurange_refactored/react/api/config/AxiosConfig.js
elif [ $1 = "auto" ];
then
	cp ./.env.example ./.env
fi

echo -e "${GRN}Downloading and setting up terraform${NC}"

# Updated Terraform to newest release June 4 2022
wget https://releases.hashicorp.com/terraform/1.2.2/terraform_1.2.2_linux_amd64.zip
unzip terraform_1.2.2_linux_amd64.zip
sudo mv terraform /usr/bin/terraform

# Check to see if docker is already installed. If it is, skip this.
if ! [ -x "$(command -v docker)" ];
then
	echo -e "${GRN}Downloading and setting up docker${NC}"
	wget -O docker.sh get.docker.com
	chmod +x docker.sh
	
	echo -e "${GRN}Creating a user group for docker, and adding your account...${NC}"
	sudo groupadd docker
	sudo usermod -aG docker $username

	./docker.sh
else
	echo "Docker already installed. Skipping Docker installation."
fi

# Initialize psql 
sudo -Hiu postgres psql -U postgres -c "alter user postgres with password '"$dbpass"';"
sudo -Hiu postgres psql -U postgres -c "CREATE DATABASE $dbname ;"


# Install the requirements for webssh
./webssh-install.sh

# Fix the script dumping us to a different directory after installation
cd $current_directory
npm run build

# Clean up
rm ./terraform_1.2.2_linux_amd64.zip
rm ./docker.sh

echo -e "${GRN}To run the app any time, use: ${NC} npm start"
echo -e "${GRN}You may need to make sure that pip-executables are accessible${NC}"
echo -e "${GRN}If the ${NC} flask ${GRN} or ${NC} celery ${GRN} commands are not recognized, try:"
echo -e "${NC}source ~/.bashrc ${GRN} or ${NC} export PATH=/home/$username/.local/bin:\$PATH ${NC}"

sudo su $USER --login
