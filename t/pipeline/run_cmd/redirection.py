import unittest, sys, os, re
from warnings import warn

root_dir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..'))
sys.path.append(os.path.join(root_dir, 'lib'))
from Pipeline.run_bowtie2 import RunBowtie2
from Pipeline.Pipeline import Pipeline
from Pipeline.host import Host
host_conf=os.path.join(root_dir, 'config', 'hosts.conf')
host=Host(host_conf, 'clutch')
working_dir=os.path.join(root_dir, 'data')

class TestBasic(unittest.TestCase):
    
    def setUp(self):
        print

    def test_bowtie2(self):
        pipeline=Pipeline('mock', host, working_dir)
        data_basename='1047-COPD.10K'
        ref_index='hg19'
        bt2=RunBowtie2(pipeline, data_basename, ref_index)
        bt2.run()

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBasic)
    unittest.TextTestRunner(verbosity=2).run(suite)

