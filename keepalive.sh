#! /bin/sh

lockf -s -t 0 /usr/local/jenkins/jenkins-slave-scripts/slave.lock \
	/usr/local/jenkins/jenkins-slave-scripts/startslave.sh >> \
	/usr/local/jenkins/jenkins-slave-scripts/slave.log 2>&1 &
