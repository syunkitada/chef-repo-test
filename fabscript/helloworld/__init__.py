# coding: utf-8
from fabric.api import env, task, hosts
from api import *
import util, conf

@task(task_class=LogTask)
@hosts('localhost')
def hello():
    run('echo helloworld')

    return 0

@task(task_class=LogTask)
@hosts('localhost')
def hello2():
    run('echo helloworld22')

    return 0
