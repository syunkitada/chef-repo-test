# coding: utf-8
from fabric.api import env, task, hosts
from api import *
import util, conf

@task
@hosts('localhost')
def hello():
    run('hostname')
    run('echo helloworld')

    return 0
