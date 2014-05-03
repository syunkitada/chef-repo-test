# coding: utf-8

from fabric.api import env, task, hosts, roles, cd
from api import *
import util, conf
from fablib.mysql import Mysql

data = None
mysql = None

@task
def setdata():
    env.roledefs.update({
        'mysql.master': [ '192.168.254.129' ],
        'mysql.slave': [ '192.168.254.131' ],
    })
    global data, mysql
    data = util.get_data_bag('hoge', 'mysql')

@task
@roles('mysql.master', 'mysql.slave')
def setup_user():
    if data:
        mysql = Mysql(data['root_password'])
        mysql.create_users(data['users'])

# mysql_dumpとmaster_log_positionの入ったmysql.tar.gzをmysql.slaveのホストに転送します
@task
@roles('mysql.master')
def dump_master():
    if data:
        mysql = Mysql(data['root_password'])
        mysql.dump_scp(env.roledefs['mysql.slave'])

@task
@roles('mysql.slave')
def setup_slave():
    if data:
        mysql = Mysql(data['root_password'])

        master_host = env.roledefs['mysql.master'][0]
        master_user = data['master_user']
        master_password = ''
        for user in data['users']:
            if user['user'] == master_user:
                master_password = user['password']
                break

        mysql.setup_slave(master_host, master_user, master_password)

@task
@roles('mysql.slave')
def show_slave_status():
    if data:
        mysql = Mysql(data['root_password'])
        mysql.sql('SHOW SLAVE STATUS\G')

