# coding: utf-8

from fabric.api import task, env, settings, shell_env, parallel
import conf, util
from api import *

@task
@parallel(pool_size=10)
def cook(option=None):
    with shell_env(PASSWORD=env.password):
        local('knife solo cook %s --sync-only --ssh-password $PASSWORD' % (env.host))
        if conf.is_proxy(option):
            with shell_env(http_proxy=conf.http_proxy, https_proxy=conf.http_proxy):
                chef_solo = sudo('chef-solo -c chef-solo/solo.rb -j chef-solo/dna.json', warn_only=True)
        else:
            chef_solo = sudo('chef-solo -c chef-solo/solo.rb -j chef-solo/dna.json', warn_only=True)

        last_cook = '%s[%d]' % (util.get_timestamp(), chef_solo.return_code)

    uptime = run('uptime')

    host_json = util.load_json()
    host_json.update({'last_cook': last_cook})
    host_json.update({'uptime': uptime})
    util.dump_json(host_json)