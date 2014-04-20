# coding: utf-8

from fabric import api
import commands

api.env.cmd_history = []

# memo
# with settings(warn_only=True): をやろうとすると失敗する (sudo: export command not found)
# warn_onlyを利用する場合は、run(cmd, warn_only=True) でやる

def run(cmd, **kwargs):
    api.env.cmd_history.append('run> ' + cmd)
    if api.env.is_test:
        return test_cmd(cmd)
    else:
        return api.run(cmd, kwargs)

def sudo(cmd, **kwargs):
    api.env.cmd_history.append('sudo> ' + cmd)
    if api.env.is_test:
        return test_cmd(cmd)
    else:
        return api.sudo(cmd, kwargs)

def local(cmd, **kwargs):
    api.env.cmd_history.append('local> ' + cmd)
    if api.env.is_test:
        return test_cmd(cmd)
    else:
        return api.local(cmd, kwargs)

def test_cmd(cmd):
    if cmd == 'uptime':
        result = commands.getoutput('uptime')
    else:
        result = cmd
    return TestCmd(result)

class TestCmd(str):
    return_code = 0
