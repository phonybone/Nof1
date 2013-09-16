import unittest, sys, os, argparse
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from pipeline import *
from Nof1Pipeline.Nof1Pipeline import Nof1Pipeline
from Pipeline.exceptions import *

class TestRunMain(unittest.TestCase):
    
    @classmethod
    def get_args(self):
        parser=argparse.ArgumentParser(description='run pipeline harness')

        parser.add_argument('--data_basename', default='test_rnaseq/rawdata/1047-COPD.1K2')
        parser.add_argument('--ref_index', default='hg19')

        parser.add_argument('--variants_fn', default='trip_neg_Vic/triple_negativ_mut_seq')

        parser.add_argument('--dry_run', default=False, action='store_true')
        parser.add_argument('--no_echo', default=False, action='store_true')
        parser.add_argument('--skip', default=False, action='store_true')
        self.args=parser.parse_args()
        print self.args

    def setUp(self):
#        host.set('dry_run', str(False))
        print

    def test_cmd(self):
        try:
            p=Nof1Pipeline(host, working_dir, 
                           self.args.data_basename, 
                           self.args.ref_index, 
                           self.args.variants_fn,
                           output_dir=output_dir, 
                           dry_run=self.args.dry_run,
                           echo=not self.args.no_echo, 
                           skip_if_current=self.args.skip)
            p.run()
        except PipelineException, e:
            print 'Failed: %s' % e.cmd.name
            print '  see %s for details' % e.cmd.get_stderr()
            self.fail(e.message)

            

if __name__=='__main__':
    TestRunMain.get_args()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestRunMain)
    unittest.TextTestRunner(verbosity=2).run(suite)

