#! /bin/sh

slavename=`hostname`

cd /jenkins || exit 1
while [ ! -f salve.dontstart ]
do
	date
	# mirror mode, update it if there's a timestamp change on the master
	fetch -m -o slave.jar https://jenkins.freebsd.org/jnlpJars/slave.jar
	java -jar slave.jar -jnlpUrl https://jenkins.freebsd.org/computer/${slavename}/slave-agent.jnlp
	sleep 30
done
