import unittest, sys, os, re, ConfigParser
from warnings import warn

dir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
sys.path.append(os.path.join(dir, 'lib'))
from Nof1.Pipeline.run_bowtie2 import RunBowtie2

class TestBasic(unittest.TestCase):
    conf=ConfigParser.ConfigParser()
    fn=os.path.join(dir, 'config', 'hosts.conf')
    conf.read(fn)
    
    def setUp(self):
        print

    def test_cmd(self):
        data_basename='1047-COPD.10K'
        ref_index='hg19'
        bt2=RunBowtie2(data_basename, ref_index, self.conf)
        cmd=bt2.cmd_string()

        self.assertIn('bowtie2', cmd)
        self.assertIn(ref_index, cmd)
        self.assertIn(data_basename, cmd)
        self.assertIn('-1', cmd)
        self.assertIn('-2', cmd)
        self.assertIn('-S', cmd)

suite = unittest.TestLoader().loadTestsFromTestCase(TestBasic)
def test_all():
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
    test_all()

