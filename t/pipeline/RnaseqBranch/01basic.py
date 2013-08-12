import unittest, sys, os, re
from cStringIO import StringIO
from warnings import warn

dir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..'))
sys.path.append(os.path.join(dir, 'lib'))
from Nof1.Pipeline.RnaseqBranch import RnaseqBranch

from Nof1.Pipeline.host import Host
host_conf=os.path.join(dir, 'config', 'hosts.conf')
host=Host(host_conf, 'clutch')
working_dir=os.path.join(dir, 'data')

class TestBasic(unittest.TestCase):
    
    def setUp(self):
        print

    def test_cmd(self):
        data_basename='1047-COPD.10K'
        ref_index='hg19'
        
        old_stdout=sys.stdout
        sys.stdout=mystdout=StringIO()
        
        host.set('dry_run', str(True))
        RnaseqBranch(host, working_dir, data_basename, ref_index).run()
        sys.stdout=old_stdout
            
        lines=mystdout.getvalue().split('\n')
        self.assertIn('bowtie2', lines[0])
        self.assertIn(data_basename, lines[0])
        self.assertIn(ref_index, lines[0])

        self.assertIn('rnaseq_count.py', lines[1])
        self.assertIn(data_basename, lines[1])

suite = unittest.TestLoader().loadTestsFromTestCase(TestBasic)
def test_all():
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
    test_all()

