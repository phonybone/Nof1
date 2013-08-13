import unittest, sys, os, re
from warnings import warn

dir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
sys.path.append(os.path.join(dir, 'lib'))
from Pipeline.run_bowtie2 import RunBowtie2

from Pipeline.host import Host
host_conf=os.path.join(dir, 'config', 'hosts.conf')
host=Host(host_conf, 'clutch')
working_dir=os.path.join(dir, 'data')

class TestBasic(unittest.TestCase):
    
    def setUp(self):
        print

    def test_bowtie2(self):
        data_basename='1047-COPD.10K'
        ref_index='hg19'
        bt2=RunBowtie2(host, working_dir, data_basename, ref_index)
        cmd=bt2.cmd_string()

        self.assertIn('bowtie2', cmd)
        self.assertIn(ref_index, cmd)
        self.assertIn(data_basename, cmd)
        self.assertIn('-1', cmd)
        self.assertIn('-2', cmd)
        self.assertIn('-S', cmd)

suite = unittest.TestLoader().loadTestsFromTestCase(TestBasic)
#def test_all():
unittest.TextTestRunner(verbosity=2).run(suite)

#if __name__ == '__main__':
#    print 'burp'
#    unittest.main()
#    test_all()

