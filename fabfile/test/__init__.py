# coding: utf-8

from fabric.api import *
import os, unittest, commands
import conf
import test_util
import test_host
import test_prepare
import test_cook
import test_node
import test_role

env.is_test = False
chef_repo_path = os.path.join(os.path.dirname(__file__), 'chef-repo')

@task
@hosts('localhost')
def test():
    env.is_test = True

    # first, remove all node, and create test nodes in test_node
    conf.init_test_conf()
    commands.getoutput('rm -r %s/*' % conf.node_path)
    suites = [
            unittest.TestLoader().loadTestsFromTestCase(test_node.TestSequenceFunctions),
            unittest.TestLoader().loadTestsFromTestCase(test_util.TestSequenceFunctions),
            unittest.TestLoader().loadTestsFromTestCase(test_host.TestSequenceFunctions),
            unittest.TestLoader().loadTestsFromTestCase(test_prepare.TestSequenceFunctions),
            unittest.TestLoader().loadTestsFromTestCase(test_cook.TestSequenceFunctions),
            unittest.TestLoader().loadTestsFromTestCase(test_role.TestSequenceFunctions),
        ]

    alltests = unittest.TestSuite(suites)
    unittest.TextTestRunner(verbosity=2).run(alltests)


