#!/bin/bash

NC='\033[0m'
red='\033[0;31m'
green='\033[0;32m'
blue='\033[0;34m'
cyan='\033[0;36m'
EDU_FOLDER='CHANGE-ME'

echo "TODO: ask for disabling mail notifications (sed on ~tasks.py:389)"
echo "TODO: read .ENV variables to set up the appropriate environment"
echo "TODO: restart gunicorn and celery (i.e. kill previous processes + start new ones)"
echo "TODO: make output more concise (i.e. be less verbose)"

function main {
	cd $EDU_FOLDER
	updateGit
	updateDocker

	: '
	while read line; do
		key=`echo $line | cut -d= -f1`
		value=`echo $line | cut -d= -f2`
	done < .env
	'

	printf "${cyan}[?] Do you want to redirect port 5000 to port 80? [y/N] ${NC}"
	read iptables

	if [[ $iptables == [yY] || $iptables == [yY][eE][sS] ]]; then
		sudo iptables -t nat -A OUTPUT -o lo -p tcp --dport 80 -j REDIRECT --to-port 5000
		sudo iptables -t nat -A PREROUTING -i eth0 -p tcp --dport 80 -j REDIRECT --to-port 5000
		echo -e "${green}[+] iptables rules added${NC}";
	fi

	echo -e "${green}[+] Update completed!${NC}"
}

function updateGit {
	echo -e "${blue}[*] Pulling git repo...${NC}"
	pull=`git pull https://github.com/edurange/edurange-flask`

	if [[ $? != 0 ]]; then
		echo -e "${red}[!] Failed to git pull edurange-flask :(${NC}"
		return
	fi

	for line in $pull; do
		if [[ $line == *"up to date"* ]]; then
			echo -e "${green}[+] You are already running the latest version. ${NC}"
			return
		fi
	done

	echo -e "${green}[+] Repo updated successfully...${NC}"
	echo -e "${blue}[*] Setting up EDURange...${NC}"

	for line in `git diff --name-only HEAD HEAD~1`; do
		if [[ $line =~ 'package.json' ]]; then
			echo -e "${cyan}[+] package.json was updated!${NC}"
			echo -e "${blue}[*] Installing npm dependencies...${NC}"
			npm install
			echo -e "${blue}[*] Building web assets...${NC}"
			npm run build
		elif [[ $line =~ 'models.py' ]]; then
			echo -e "${cyan}[+] The user model was updated!${NC}"
			echo -e "${blue}[*] Running migrations...${NC}"
			flask db migrate
			flask db upgrade
		fi
	done
}

function updateDocker {
	echo -e "${blue}[*] Pulling docker image...${NC}"
	docker image pull sanivo/edurange-ubuntu-sshd:16.04
}

main
