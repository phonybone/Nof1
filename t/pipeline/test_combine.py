import unittest, sys, os, re
from warnings import warn

dir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
sys.path.append(os.path.join(dir, 'lib'))
from Pipeline.run_combine import RunCombine

from Pipeline.host import Host
host_conf=os.path.join(dir, 'config', 'hosts.conf')
host=Host(host_conf, 'clutch')
working_dir=os.path.join(dir, 'data')

class TestBasic(unittest.TestCase):
    
    def setUp(self):
        print

    def test_combine(self):
        data_basename='1047-COPD.10K'
        variants_fn='triple_negativ_mut_seq'
        comb=RunCombine(host, working_dir, 
                        data_basename, variants_fn,
                        )
        cmd=comb.cmd_string()
        print cmd

        self.assertIn(host.get('combine.script'), cmd)
        self.assertIn(data_basename, cmd)
        self.assertIn(variants_fn, cmd)


suite = unittest.TestLoader().loadTestsFromTestCase(TestBasic)
#def test_all():
unittest.TextTestRunner(verbosity=2).run(suite)

#if __name__ == '__main__':
#    print 'burp'
#    unittest.main()
#    test_all()

