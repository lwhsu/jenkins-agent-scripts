#! /bin/sh

export PATH="/sbin:/bin:/usr/sbin:/usr/bin:/usr/local/sbin:/usr/local/bin"

cd /jenkins/jenkins-slave-scripts || exit 1

if [ -r agent.conf ]; then
	. agent.conf
fi

for i in master secret; do
	eval v=\$$i
	if [ -z ${v} ]; then
		echo "${i} is not defined" >&2
		exit 1
	fi
done

slavename=`/bin/hostname`

while [ ! -f slave.dontstart ]
do
	/bin/date
	# mirror mode, update it if there's a timestamp change on the master
	/usr/bin/fetch -m -o slave.jar https://${master}/jnlpJars/slave.jar
	/usr/local/bin/java -Djava.net.preferIPv6Addresses=true \
		-jar slave.jar \
		-jnlpUrl https://${master}/computer/${slavename}/slave-agent.jnlp \
		-secret ${secret}
	/bin/sleep 30
done
