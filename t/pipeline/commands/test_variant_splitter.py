import unittest, sys, os, argparse

root_dir=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
print 'root_dir is %s' % root_dir
sys.path.append(os.path.join(root_dir, 't'))
from pipeline import *
from Pipeline.host import Host

from Nof1Pipeline.run_variant_splitter import RunVariantSplitter

class TestBasic(unittest.TestCase):
    
    @classmethod
    def get_args(self):
        parser=argparse.ArgumentParser()
        parser.add_argument('--host')
        self.args=parser.parse_args()
        
    def setUp(self):
        print

    def test_variant_splitter(self):
        host=Host(hostname=self.args.host)
        pipeline=Pipeline('mock', host, working_dir, True)
        data_basename='data/rawdata/1047-COPD.10K'
        variants_fn='data/trip_neg_Vic/triple_negativ_mut_seq'
        output_dir=os.path.join(root_dir, 't', 'fixtures', 'var2reads')
        cmd=RunVariantSplitter(pipeline, data_basename, variants_fn, output_dir)
        cmd=cmd.cmd_string()
        print cmd

        self.assertIn(host.get('variant_splitter.script'), cmd)
        self.assertIn(data_basename, cmd)
        self.assertIn(variants_fn, cmd)



if __name__ == '__main__':
    TestBasic.get_args()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBasic)
    unittest.TextTestRunner(verbosity=2).run(suite)

