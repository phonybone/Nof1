import unittest, sys, os
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from pipeline import *
from Pipeline.Nof1Pipeline import Nof1Pipeline
from cStringIO import StringIO

class TestBasic(unittest.TestCase):
    
    def setUp(self):
        host.set('dry_run', str(True))
        print

    def test_cmd(self):
        data_basename='data/test_rnaseq/rawdata/1047-COPD.10K'
        ref_index='hg19'
    	variants_fn='data/trip_neg_Vic/triple_negativ_mut_seq'

        old_stdout=sys.stdout
        sys.stdout=mystdout=StringIO()
        
        p=Nof1Pipeline(host, working_dir, data_basename, ref_index, variants_fn, dry_run=True)
        p.run()
        sys.stdout=old_stdout
            
        lines=mystdout.getvalue().split('\n')
        for l in lines:
            print l

if __name__=='__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBasic)
    unittest.TextTestRunner(verbosity=2).run(suite)

