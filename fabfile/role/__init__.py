# coding: utf-8

from fabric.api import *
import commands
import util, conf

@task
def role(reg_role='*'):
    roles = commands.getoutput('find %s/*.rb' % (conf.roles_path))
    print roles
