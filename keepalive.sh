#! /bin/sh

lockf -s -t 0 /jenkins/jenkins-slave-scripts/slave.lock \
	/jenkins/jenkins-slave-scripts/startslave.sh >> \
	/jenkins/jenkins-slave-scripts/slave.log 2>&1 &
