#!/bin/bash

GRN='\033[0;32m'
NC='\033[0m'

TEMPLATE_FOLDER=scenario_template_files
echo -e "${GRN}Please enter the name for your new scenario:\n${NC}"
read SCENARIO_NAME

SCENARIO_PATH=../prod/$SCENARIO_NAME

echo -e "${GRN}Creating scenario folder...\n${NC}"
mkdir -p -v $SCENARIO_PATH

echo -e "${GRN}Please enter the number of containers you will need${NC}"
read CONTAINER_COUNT

for (( c=1; c<=$CONTAINER_COUNT; c++ ))
do
	echo -e "${GRN} Enter a name for container number $c ${NC}"
	read CONTAINER_NAME
	CONTAINER_PATH=$SCENARIO_PATH/$CONTAINER_NAME.tf.json
	cp $TEMPLATE_FOLDER/container_name.tf.json $CONTAINER_PATH

	echo -e "${GRN}Enter a hostname for this container${NC}"
	ADDR=$(( $c+1 ))
	sed -i "s/SNAME/$SCENARIO_NAME/g" $CONTAINER_PATH
	sed -i "s/|cName|/$CONTAINER_NAME/g" $CONTAINER_PATH
	sed -i "s/ADDR1/$ADDR/g" $CONTAINER_PATH
	sed -i "s/ADDR2/$ADDR/g" $CONTIANER_PATH

	echo -e "${GRN} Enter a docker image name to use ${NC}"
	echo -e "${GRN} Ex: edurange2/ubuntu_sshd:16.04 ${NC}"
	read $IMAGE
	sed -i "s/|image path|/$IMAGE/g" $CONTAINER_PATH
done

echo -e "${GRN}Copying remaining files...\n${NC}"


