#!/usr/local/bin/python3

#-
# Copyright (c) 2018 The FreeBSD Foundation
#
# This software was developed by Li-Wen Hsu under sponsorship from
# the FreeBSD Foundation.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR AND CONTRIBUTORS ``AS IS'' AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY
# OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
# SUCH DAMAGE.

import json
import socket
import subprocess
import time
import urllib.request

jenkins_url = "https://ci.example.org"
computer = socket.gethostname()

url = "{}/computer/{}/api/json?tree=executors[currentExecutable[url]]".format(
        jenkins_url, computer)

while True:
    url_data = urllib.request.urlopen(url)
    content = url_data.read()
    json_data = json.loads(content.decode('utf-8'))
    executors = json_data['executors']

    in_exec = set()
    for e in executors:
        if e['currentExecutable'] is not None:
            build_url = e['currentExecutable']['url']
            job_name = build_url.split('/')[4]
            in_exec.add(job_name)

    jail_base = 'zroot/jenkins/jails'
    cmd = 'zfs list -Hr {}'.format(jail_base)
    p = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    for line in p.stdout:
        jail_fs = line.split()[0].decode('utf-8')
        if jail_fs == jail_base:
            continue
        jail_job_name = jail_fs.split('/')[3]
        if jail_job_name not in in_exec:
            print('delete {}'.format(jail_fs))
            cmd_destroy = 'zfs destroy {}'.format(jail_fs)
            p2 = subprocess.Popen(cmd_destroy.split(), stdout=subprocess.PIPE)

    time.sleep(600)
