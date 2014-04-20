# coding: utf-8

import conf, util
from fabric.api import *

@task
@hosts('localhost')
def host(host_pattern=None):
    env.hosts = util.get_available_hosts(host_pattern)

    if not env.is_test:
        print 'set up targets'
        for host in env.hosts:
            print host

        print '\nis ok?\nif you ok, enter your password\n'
        sudo('hostname')
