# coding: utf-8

from api import *

class Mysql:
    root_password_key = 'mysql_root_password'

    def __init__(self, root_password):
        set_pass(self.root_password_key, root_password)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass
        # unset_pass()

    def sql(self, query, additional_cmd=''):
        return run('mysql -uroot -p%s -e "%s" %s' % (get_pass(self.root_password_key), query, additional_cmd))

    def sqlfile(self, file_path):
        return run('mysql -uroot -p%s < %s' % (get_pass(self.root_password_key), file_path))

    def dump(self, dumpfile):
        return run('mysqldump -uroot -p%s --all-databases > %s' % (get_pass(self.root_password_key), dumpfile))

