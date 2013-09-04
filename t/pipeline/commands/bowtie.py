import unittest, sys, os, re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from pipeline import *

from Nof1Pipeline.run_bowtie2 import RunBowtie2

class TestBasic(unittest.TestCase):
    
    def setUp(self):
        print

    def test_bowtie2(self):
        pipeline=Pipeline('mock', host, working_dir, True)
        data_basename='1047-COPD.10K'
        ref_index='hg19'
        bt2=RunBowtie2(pipeline, data_basename, ref_index)
        cmd=bt2.cmd_string()
        print cmd

        self.assertIn('bowtie2', cmd)
        self.assertIn(ref_index, cmd)
        self.assertIn(data_basename, cmd)
        self.assertIn('-1', cmd)
        self.assertIn('-2', cmd)
        self.assertIn('-S', cmd)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBasic)
    unittest.TextTestRunner(verbosity=2).run(suite)

