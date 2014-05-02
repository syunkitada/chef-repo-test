# coding: utf-8

from fabric.api import env, task, hosts
from api import *
import util, conf

@task
def user():
    data = util.get_data_bag('hoge', 'mysql')

    set_pass('mysql_root_password', data['root_password'])
    print 'test'

    for user in data['users']:
        create_user(user)

    unset_pass()

def create_user(user):
    sqlcmd = ''
    print 'test'
    set_pass('mysql_user_password', user['password'])
    for host in user['hosts']:
        sqlcmd += "GRANT %(grant)s PRIVILEGES ON *.* TO %(user)s@%(host)s IDENTIFIED BY '%(mysql_user_password)s' WITH GRANT OPTION;" \
                    % dict(user, **{'host': host, 'mysql_user_password': get_pass('mysql_user_password')})

    sql(sqlcmd)

def sql(sqlcmd):
    run('mysql -uroot -p%s -e "%s"' % (get_pass('mysql_root_password'), sqlcmd))
