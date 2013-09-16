import unittest, sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
from pipeline import *
from Nof1Pipeline.Nof1Pipeline import Nof1Pipeline

import argparse


class TestShowMain(unittest.TestCase):

    @classmethod
    def get_args(self):
        parser=argparse.ArgumentParser()
        parser.add_argument('--skip', action='store_true')
        self.args=parser.parse_args()
        
    def setUp(self):
        host.set('dry_run', str(True))
        print

    def test_cmd(self):
#        data_basename='test_rnaseq/rawdata/1047-COPD.10K' # clutch
        data_basename='rawdata/1047-COPD.10K' # buffy
        ref_index='hg19'
    	variants_fn='trip_neg_Vic/triple_negativ_mut_seq'

        p=Nof1Pipeline(host, working_dir, data_basename, ref_index, variants_fn, 
                       dry_run=True, skip_if_current=self.args.skip)
        print '# Running pipeline %s' % p.name
        p.check_continuity()
        print '# continuity check ok'
        print
        p.run()


if __name__=='__main__':
    TestShowMain.get_args()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestShowMain)
    unittest.TextTestRunner(verbosity=2).run(suite)

