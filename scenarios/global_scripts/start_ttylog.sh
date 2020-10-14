#!/bin/bash

if [ -z "$SSH_ORIGINAL_COMMAND" ]; then
	TTY_CMD=$(tty)
	TTY=${TTY_CMD:5}
	HOST=$(hostname)
	#HOST=$(echo $HN | awk -F. '{print $(NF - 2)}')
	#EXP=$(echo $HN | awk -F. '{print $(NF - 1)}')
	#PROJ=$(echo $HN | awk -F. '{print $(NF)}')
	USER=$(whoami)
	LOGDIR=/usr/local/src/logs

	if [ -e "${LOGDIR}/count.$HOST" ]; then
		CNT=$(cat $LOGDIR/count."$HOST")
		((CNT++))
		echo $CNT > $LOGDIR/count."$HOST"
	else
		sudo touch $LOGDIR/count."$HOST"
		sudo chmod ugo+rw $LOGDIR/count."$HOST"
		echo "0" > $LOGDIR/count."$HOST"
		CNT=$(cat $LOGDIR/count."$HOST")
	fi

	export TTY_SID=$CNT
	export TTY_USER=$USER
	LOGPATH=$LOGDIR/ttylog.$HOST.$USER.$CNT

	sudo touch "$LOGPATH"
	sudo chmod ugo+rw "$LOGPATH"

	echo "starting session w tty_sid:$CNT" >> "$LOGPATH"
	echo "User prompt is ${USER}@${HOST}" >> "$LOGPATH"
	echo "Home directory is ${HOME}" >> "$LOGPATH"

	sudo /usr/local/src/ttylog/ttylog "$TTY" >> $LOGPATH 2>/dev/null &

	bash
	echo "END tty_sid:$CNT" >> "$LOGPATH"

elif [ "$(echo ${SSH_ORIGINAL_COMMAND} | grep '^sftp' )" ]; then

	#sudo touch /var/log/tty.log
	#sudo chmod ugo+rw /var/log/tty.log
	#echo "$SSH_ORIGINAL_COMMAND" >> /var/log/tty.log
	/usr/lib/openssh/sftp-server
	#exec ${SSH_ORIGINAL_COMMAND}

elif [ "$(echo ${SSH_ORIGINAL_COMMAND} | grep '^scp' )" ]; then

	#HN=$(cat /var/emulab/boot/nickname)
	#HOST=$(echo $HN | awk -F. '{print $(NF - 2)}')
	#EXP=$(echo $HN | awk -F. '{print $(NF - 1)}')
	#PROJ=$(echo $HN | awk -F. '{print $(NF)}')

	#LOGPATH=/var/log/ttylog/ttylog.null.$HOST
	#touch $LOGPATH
	#echo "$SSH_ORIGINAL_COMMAND" >> $LOGPATH
	exec ${SSH_ORIGINAL_COMMAND}

elif [ "$(echo ${SSH_ORIGINAL_COMMAND})" ]; then

	#HN=$(cat /var/emulab/boot/nickname)
	#HOST=$(echo $HN | awk -F. '{print $(NF - 2)}')
	#EXP=$(echo $HN | awk -F. '{print $(NF - 1)}')
	#PROJ=$(echo $HN | awk -F. '{print $(NF)}')

	#LOGPATH=/var/log/ttylog/ttylog.null.$HOST
	#echo "$SSH_ORIGINAL_COMMAND" >> $LOGPATH
	exec ${SSH_ORIGINAL_COMMAND}

	TMPPATH=/tmp/sshcmds.sh
	$(echo $SSH_ORIGINAL_COMMAND >> $TMPPATH)
	bash $TMPPATH
	rm $TMPPATH

fi
