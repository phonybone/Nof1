import unittest, sys, os, re
from warnings import warn

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from pipeline import *

from Nof1Pipeline.run_variant_count import RunVariantCount

class TestBasic(unittest.TestCase):
    
    def setUp(self):
        print

    def test_variant_count(self):
        pipeline=Pipeline('mock', host, working_dir, True)
        data_basename='data/rawdata/1047-COPD'
        variants_fn='data/trip_neg_Vic/triple_negativ_mut_seq'

        cmd=RunVariantCount(pipeline, data_basename, variants_fn)
        cmd=cmd.cmd_string()
        print cmd

        self.assertIn(host.get('variant_count.script'), cmd)
        self.assertIn(data_basename, cmd)
        self.assertIn(variants_fn, cmd)



if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBasic)
    unittest.TextTestRunner(verbosity=2).run(suite)

