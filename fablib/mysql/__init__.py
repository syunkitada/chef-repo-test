# coding: utf-8

from fabric.api import cd
from api import *

class Mysql:
    root_password_key = 'mysql_root_password'
    dump_directory = 'mysql_working_directory'
    dump_file = 'dbdump.db'
    master_status_file = 'master_status'

    def __init__(self, root_password):
        set_pass(self.root_password_key, root_password)

    def __del__(self):
        unset_pass()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        unset_pass()

    def sql(self, query, additional_cmd=''):
        return run('mysql -uroot -p%s -e "%s" %s' % (get_pass(self.root_password_key), query, additional_cmd))

    def sqlfile(self, file_path):
        return run('mysql -uroot -p%s < %s' % (get_pass(self.root_password_key), file_path))

    def create_users(self, users):
        for user in users:
            set_pass('mysql_user_password', user['password'])
            self.sql(self.__get_query_create_user(user))

    def __get_query_create_user(self, user):
        sqlcmd = ''
        for host in user['hosts']:
            sqlcmd += "GRANT %(grant)s ON *.* TO %(user)s@%(host)s IDENTIFIED BY \\\"%(mysql_user_password)s\\\" WITH GRANT OPTION;" \
                        % dict(user, **{'host': host, 'mysql_user_password': get_pass('mysql_user_password')})

        return sqlcmd

    def dump(self, dumpfile):
        return run('mysqldump -uroot -p%s --all-databases > %s' % (get_pass(self.root_password_key), dumpfile))

    def dump_scp(self, to_hosts):
        run('rm -rf %s' % self.dump_directory)
        run('mkdir %s' % self.dump_directory)
        self.sql('FLUSH TABLES WITH READ LOCK')
        self.sql('SHOW MASTER STATUS',
                '| grep log-bin > %s/%s' % (self.dump_directory, self.master_status_file))
        self.dump('%s/%s' % (self.dump_directory, self.dump_file))
        self.sql('UNLOCK TABLES')
        run('tar czvf %s.tar.gz %s' % (self.dump_directory, self.dump_directory))

        for host in to_hosts:
            scp('%s.tar.gz' % self.dump_directory, '%s:~/' % host)

        run('rm -rf %s*' % self.dump_directory)

    def setup_slave(self, master_host, master_user, master_password):
        run('tar xvf %s.tar.gz' % self.dump_directory)
        with cd(self.dump_directory):
            master_log_file = run("cat %s | awk '{print $1}'" % self.master_status_file)
            master_log_pos = run("cat %s | awk '{print $2}'" % self.master_status_file)
            self.sqlfile('dbdump.db')
            self.sql('STOP SLAVE')
            self.sql('''
                CHANGE MASTER TO
                MASTER_HOST='%(master_host)s',
                MASTER_USER='%(master_user)s',
                MASTER_PASSWORD='%(master_password)s',
                MASTER_LOG_FILE='%(master_log_file)s',
                MASTER_LOG_POS=%(master_log_pos)s;''' % locals())
            self.sql('START SLAVE')
            run('rm -rf %s*' % self.dump_directory)

