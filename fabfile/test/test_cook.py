import unittest
from cook import cook
from fabric.api import env
import conf

class TestSequenceFunctions(unittest.TestCase):
    def test_cook(self):
        conf.init_test_conf()
        cook('p')
        cmd_history = [
            'local> knife solo cook %s --sync-only --ssh-password $PASSWORD' % (env.host),
            'sudo> chef-solo -c chef-solo/solo.rb -j chef-solo/dna.json',
            'run> uptime'
                ]
        self.assertEqual(cmd_history, env.cmd_history)
        self.assertTrue(env.is_proxy)

        env.cmd_history = []
        cook()
        self.assertEqual(cmd_history, env.cmd_history)
        self.assertFalse(env.is_proxy)
