import unittest, sys, os
from Nof1Pipeline.Nof1Pipeline import Nof1Pipeline

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from pipeline import *

class TestBasic(unittest.TestCase):
    
    def setUp(self):
        host.set('dry_run', str(True))
        print

    def test_cmd(self):
        data_basename='test_rnaseq/rawdata/1047-COPD.10K'
        ref_index='hg19'
    	variants_fn='trip_neg_Vic/triple_negativ_mut_seq'

        p=Nof1Pipeline(host, working_dir, data_basename, ref_index, variants_fn, 
                       dry_run=True, skip_if_current=False)
        p.run()


if __name__=='__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBasic)
    unittest.TextTestRunner(verbosity=2).run(suite)

