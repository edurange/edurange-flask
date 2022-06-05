#!/bin/bash

GRN='\033[0;32m'
YLW='\033[1;33m'
NC='\033[0m'
username=$(whoami)
current_directory=$(pwd)
dbpass="passwordfoo"
dbname="namefoo"
# Add pip-executables to the path if they aren't already
if [ grep -q "export PATH=/home/$(whoami)/.local/bin:$PATH" ~/.bashrc ]; 
then
	:
else
	echo "export PATH=/home/$(whoami)/.local/bin:$PATH" >> ~/.bashrc &&
	source ~/.bashrc
fi

echo -e "${GRN}Installing python3-pip, npm, redis-server,  unzip, postgresql, lib-pq-dev, and wget${NC}"

sudo apt update
sudo apt install -y python3-pip npm redis-server unzip wget postgresql libpq-dev
pip3 install -r requirements/prod.txt

npm install
mkdir data
mkdir data/tmp
mkdir logs

# Add option for automatic install for testing. Do not use this in a production environment.

echo "-------------------------------------"
echo $#
if [ $# -eq 0 ];
then
	echo -e "${YLW}Please enter your database password, as written in the '.env' file in the DATABASE_URL field:${NC}"
	read dbpass
	echo -e "${YLW}Please enter your database name, as written at the end of that same DATABASE_URL:${NC}"
	read dbname
elif [ $1 = "auto" ];
then
	cp ./.env.example ./.env
fi
echo "-------------------------------------"
echo "Pass: $dbpass , Name: $dbname"


echo -e "${GRN}Downloading and setting up terraform${NC}"

# Updated Terraform to newest release June 4 2022
wget https://releases.hashicorp.com/terraform/1.2.2/terraform_1.2.2_linux_amd64.zip
unzip terraform_1.2.2_linux_amd64.zip
sudo mv terraform /usr/bin/terraform

# Check to see if docker is already installed. If it is, skip this.
dinstall=$(docker -v)
echo "-------------------------------------"
echo "Docker install value: $dinstall"
if [[ -z $dinstall ]];
then
	echo -e "${GRN}Downloading and setting up docker${NC}"
	wget -O docker.sh get.docker.com
	chmod +x docker.sh
	
	echo -e "${GRN}Creating a user group for docker, and adding your account...${NC}"
	sudo groupadd docker
	sudo usermod -aG docker $username
	sudo su $USER --login

	./docker.sh
else
	echo "Docker already installed. Skipping Docker installation."
fi
sudo -Hiu postgres psql -U postgres -c "alter user postgres with password '"$dbpass"';"
#sudo -H -u postgres bash -c "echo -e ALTER USER postgres WITH PASSWORD \'$dbpass\'\; | psql"
sudo -Hiu postgres psql -U postgres -c "CREATE DATABASE $dbname ;"
#sudo -H -u postgres bash -c "echo -e CREATE DATABASE $dbname\; | psql"

# Install the requirements for webssh
./webssh-install.sh

# Fix the script dumping us to a different directory after installation
cd $current_directory
npm run build


#echo -e "${GRN}Done! Next run the first-run setup: ${NC} npm run build"
echo -e "${GRN}To run the app any time, use: ${NC} npm start"
echo -e "${GRN}You may need to make sure that pip-executables are accessible${NC}"
echo -e "${GRN}If the ${NC} flask ${GRN} or ${NC} celery ${GRN} commands are not recognized, try:"
echo -e "${NC}source ~/.bashrc ${GRN} or ${NC} export PATH=/home/$username/.local/bin:\$PATH ${NC}"

if [ $1 == "auto" ];
then
	npm start
fi