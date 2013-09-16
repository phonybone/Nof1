import unittest, sys, os, re
from warnings import warn

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from pipeline import *

from Nof1Pipeline.run_rnaseq_count import RunRnaseqCount

class TestBasic(unittest.TestCase):
    
    def setUp(self):
        print

    def test_rnaseq_count(self):
        pipeline=Pipeline('mock', host, working_dir, True)
        data_basename='t/fixtures/1047-COPD.10K'

        cmd=RunRnaseqCount(pipeline, data_basename)
        cmd=cmd.cmd_string()
        print cmd

        self.assertIn(host.get('rnaseq_count.script'), cmd)
        self.assertIn(data_basename, cmd)




if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBasic)
    unittest.TextTestRunner(verbosity=2).run(suite)

