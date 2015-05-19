#! /bin/sh

lockf -s -t 0 /jenkins/slave.lock /jenkins/startslave.sh >> /jenkins/slave.log 2>&1 &
