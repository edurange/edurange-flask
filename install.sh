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

npm install
mkdir data
mkdir data/tmp
mkdir logs

# Add option for automatic install for testing. Do not use this in a production environment.

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
	echo -e "${YLW}Please enter your external address (Like example.com):${NC}"
	read hostAddress
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

# Upgrade NodeJS from version 12 to 16
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.1/install.sh | bash
sudo apt install nodejs -y

# Raise the limit on number of file watchers for the system
echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf && sudo sysctl -p