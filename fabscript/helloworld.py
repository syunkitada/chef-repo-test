# coding: utf-8
from fabric.api import env, task, hosts
from api import *
import util, conf

@task
@hosts('localhost')
def hello():
    set_pass('mysqlpass', 'phogepass')
    set_pass('mysqlpass', 'piyogepass')
    set_pass('rootpass', 'roothogepass')
    run('echo %s' % get_pass('amysqlpass'))
    run('echo %s' % get_pass('rootpass'))
    unset_pass()

