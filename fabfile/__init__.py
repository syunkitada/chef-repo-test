# coding: utf-8
from fabric.api import *
import re, os, json, commands

env.forward_agent = True

PWD           = os.environ['PWD']
PATH_TO_NODES = PWD + '/nodes'
PATH_TO_ROLES = PWD + '/roles'

def node(reg_host='*'):
	hosts = __get_hosts(reg_host)
	host = 'HostName'
	uptime = 'Uptime'
	last_cook = 'LastCook'
	run_list = 'RunList'
	print '%(host)-25s%(uptime)-15s%(last_cook)-25s%(run_list)s' % locals()
	print '----------------------------------------------------------------------------'
	for host in hosts:
		path = '%s/%s.json' % (PATH_TO_NODES, host)
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
		print '%(host)-25s%(uptime)-15s%(last_cook)-25s%(run_list)s' % locals()

def role(reg_role='*'):
	roles = commands.getoutput('find %s/*.rb' % (PATH_TO_ROLES))
	print roles

def cook():
	with shell_env(PASSWORD=env.password):
		local('knife solo cook %s --ssh-password $PASSWORD' % (env.host))

	path = '%s/%s.json' % (PATH_TO_NODES, env.host)
	with open(path, 'r') as f:
		host_json = json.load(f)

	date = run('date +"%Y-%m-%d %I:%M:%S"')
	host_json.update({'last_cook': date})

	uptime = run('uptime')
	host_json.update({'uptime': uptime})

	with open(path, 'w') as f:
		json.dump(host_json, f)

def prepare():
	with shell_env(PASSWORD=env.password):
		local('knife solo prepare %s --ssh-password $PASSWORD' % (env.host))

# hostsの設定と、sudo passwordの設定を行う
# cook prepareをする場合は必ず実行
@hosts('localhost')
def h(*xargs):
	sudo('hostname')
	env.hosts = __get_hosts(xargs)

def __get_hosts(xargs):
	hosts = set()
	prog = re.compile('%s/(.*).json' % PATH_TO_NODES)
	for reg_host in xargs:
		host_jsons = commands.getoutput('find %s/ -name %s.json' % (PATH_TO_NODES, reg_host))
		hosts.update(set(prog.findall(host_jsons)))
	return hosts
