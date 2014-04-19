# coding: utf-8
from fabric.api import *
import re, os, json, commands
import conf
import datetime

env.forward_agent = True

def complement_path(path):
    if path.find('/') == 0:
        return path
    else:
        return os.path.join(os.path.dirname(__file__), path)

chef_repo_path = complement_path(conf.chef_repo_path)
nodes_path     = complement_path(conf.nodes_path)
role_path      = complement_path(conf.roles_path)
chef_rpm_path  = complement_path(conf.chef_rpm_path)
log_dir_path   = complement_path(conf.log_dir_path)

if not os.path.exists(log_dir_path):
    make_log_dir = commands.getoutput('mkdir %s' % (log_dir_path))

is_proxy = hasattr(conf, 'http_proxy') and conf.http_proxy != '' and hasattr(conf, 'https_proxy') and conf.http_proxy != ''

@task
def node(reg_host='*'):
    hosts = __get_hosts(reg_host)
    if len(hosts):
        print 'TODO print host info'

    host = 'HostName'
    uptime = 'Uptime'
    last_cook = 'LastCook'
    run_list = 'RunList'
    print '%(host)-40s%(uptime)-15s%(last_cook)-25s%(run_list)s' % locals()
    print '-------------------------------------------------------------------------------------------'
    for host in hosts:
        path = '%s/%s.json' % (nodes_path, host)
        with open(path, 'r') as f:
            host_json = json.load(f)
        ip_address = host_json.get('ip_address')
        uptime = host_json.get('uptime', '')
        prog = re.compile('^.*up (.+),.*user.*$')
        progs = prog.search(uptime)
        if progs:
            uptime = progs.group(1)
        last_cook = host_json.get('last_cook')
        run_list = host_json.get('run_list')
        print '%(host)-40s%(uptime)-15s%(last_cook)-25s%(run_list)s' % locals()

@task
def role(reg_role='*'):
    roles = commands.getoutput('find %s/*.rb' % (roles_path))
    print roles

@task
def cook(option=None):
    date = run('date +"%Y-%m-%d %I:%M:%S"')
    with shell_env(PASSWORD=env.password):
        local('knife solo cook %s --sync-only --ssh-password $PASSWORD' % (env.host))
        with settings(warn_only=True):
            if option and option == 'p' and is_proxy:
                with shell_env(http_proxy=conf.http_proxy, https_proxy=conf.http_proxy):
                    chef_solo = sudo('chef-solo -c chef-solo/solo.rb -j chef-solo/dna.json')
            else:
                chef_solo = sudo('chef-solo -c chef-solo/solo.rb -j chef-solo/dna.json')

            last_cook = '%s[%d]' % (date, chef_solo.return_code)
            with open(os.path.join(log_dir_path, env.host), 'w') as f:
                f.write(chef_solo)

    path = '%s/%s.json' % (nodes_path, env.host)
    with open(path, 'r') as f:
        host_json = json.load(f)

    host_json.update({'last_cook': last_cook})

    uptime = run('uptime')
    host_json.update({'uptime': uptime})

    with open(path, 'w') as f:
        json.dump(host_json, f)

@task
def prepare(option=None):
    if hasattr(conf, 'chef_rpm_path') and chef_rpm_path != '':
        chef_rpm = 'tmp_chef.rpm'
        if os.path.exists(chef_rpm_path):
            local('scp %s %s:~/%s' % (chef_rpm_path, env.host, chef_rpm))
            with settings(ok_ret_codes=[0,1]):
                if option and option == 'p' and is_proxy:
                    with shell_enb(http_proxy=conf.http_proxy, https_proxy=conf.http_proxy):
                        sudo('yum install %s -y' % chef_rpm)
                else:
                    sudo('yum install %s -y' % chef_rpm)
                run('rm -rf %s' % chef_rpm)
        else:
            print 'cannot access %s' % chef_rpm_path
    else:
        with shell_env(PASSWORD=env.password):
            local('knife solo prepare %s --ssh-password $PASSWORD' % (env.host))

    path = '%s/%s.json' % (nodes_path, env.host)
    with open(path, 'r') as f:
        host_json = json.load(f)

    host_json.update({'last_cook': 'prepared'})

    uptime = run('uptime')
    host_json.update({'uptime': uptime})

    with open(path, 'w') as f:
        json.dump(host_json, f)

# hostsの設定と、sudo passwordの設定を行う
# cook prepareをする場合は必ず実行
@task
@hosts('localhost')
def h(reg_host):
    env.hosts = __get_hosts(reg_host)
    print 'set up targets'
    print env.hosts
    print '\nis ok?\nif you ok, enter your password.\n'
    sudo('hostname')

def __get_hosts(reg_host):
    hosts = set()
    prog = re.compile('%s/(.*).json' % nodes_path)
    host_jsons = commands.getoutput('find %s/ -name %s.json' % (nodes_path, reg_host))
    hosts.update(set(prog.findall(host_jsons)))
    return hosts
