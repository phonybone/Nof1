import unittest, sys, os, argparse
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from pipeline import *
from Pipeline.Nof1Pipeline import Nof1Pipeline

class TestBasic(unittest.TestCase):
    
    def setUp(self):
#        host.set('dry_run', str(False))
        print

    def test_cmd(self):
        data_basename='test_rnaseq/rawdata/1047-COPD.1K'
        ref_index='hg19'
    	variants_fn='trip_neg_Vic/triple_negativ_mut_seq'

        Nof1Pipeline(host, working_dir, data_basename, ref_index, variants_fn,
                     output_dir=output_dir, 
                     dry_run=args.dry_run,
                     echo=not args.no_echo, 
                     skip_if_current=args.skip).run()
            

if __name__=='__main__':
    parser=argparse.ArgumentParser(description='run pipeline harness')
    parser.add_argument('--dry_run', default=False, action='store_true')
    parser.add_argument('--no_echo', default=True, action='store_false')
    parser.add_argument('--skip', default=False, action='store_true')
    args=parser.parse_args()

    suite = unittest.TestLoader().loadTestsFromTestCase(TestBasic)
    unittest.TextTestRunner(verbosity=2).run(suite)

