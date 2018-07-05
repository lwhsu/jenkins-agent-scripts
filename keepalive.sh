#! /bin/sh

lockf -s -t 0 /jenkins/jenkins-agent-scripts/agent.lock \
	/jenkins/jenkins-agent-scripts/startagent.sh >> \
	/jenkins/jenkins-agent-scripts/agent.log 2>&1 &
