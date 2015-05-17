#! /bin/sh

lockf -s -t 0 /home/jenkins/slave.lock /home/jenkins/startslave.sh >> /home/jenkins/slave.log 2>&1 &
