# coding: utf-8

import os
import ConfigParser
from fabric.api import env
import commands

inifile = ConfigParser.SafeConfigParser()
inifile_dir = os.path.join(os.path.dirname(__file__), '../../')
inifile_path = os.path.join(inifile_dir, 'fabfile.ini')
inifile.read(inifile_path)

def complement_path(path):
    if path == '':
        return None
    if path.find('/') == 0:
        return path
    else:
        return os.path.join(inifile_dir, path)

# common
chef_repo_path = complement_path(inifile.get('common', 'chef_repo_path'))
tmp_cookbooks_paths = inifile.get('common', 'cookbooks_paths')
tmp_cookbooks_paths = tmp_cookbooks_paths.replace(' ', '').split(',')
cookbooks_paths = []
for path in tmp_cookbooks_paths:
    cookbooks_paths.append(complement_path(path))

node_path      = complement_path(inifile.get('common', 'node_path'))
role_path      = complement_path(inifile.get('common', 'role_path'))
http_proxy     = inifile.get('common', 'http_proxy')
https_proxy    = inifile.get('common', 'https_proxy')

# chefric
chefric_path       = inifile.get('chefric', 'chefric_path')
log_dir_path       = os.path.join(chefric_path, inifile.get('chefric', 'chefric_log'))
chef_rpm           = inifile.get('chefric', 'chef_rpm')
chef_rpm_path      = os.path.join(chefric_path, chef_rpm)
tmp_chef_rpm       = inifile.get('chefric', 'tmp_chef_rpm')

template_json  = { 'run_list': [] }

if not os.path.exists(log_dir_path):
    os.mkdir(log_dir_path)

env.is_proxy = False
def is_proxy(option=None):
    if option and option == 'p':
        if http_proxy and https_proxy:
            env.is_proxy = True
            return True
        else:
            raise Exception('http_proxy is bad')
    else:
        env.is_proxy = False
        return False

def init_test_conf():
    env.cmd_history = []
    global chef_repo_path
    global node_path
    global role_path
    global chef_rpm_path
    global log_dir_path
    global http_proxy
    global https_proxy
    chef_repo_path = os.path.join(os.path.dirname(__file__), '../test/chef-repo')
    node_path      = os.path.join(chef_repo_path, 'node')
    role_path      = os.path.join(chef_repo_path, 'role')
    chef_rpm_path  = os.path.join(chef_repo_path, 'test-chef.rpm')
    log_dir_path   = '/tmp/chef-testlog'
    http_proxy     = 'test.proxy'
    https_proxy    = 'test.proxy'

    if not os.path.exists(log_dir_path):
        os.mkdir(log_dir_path)
