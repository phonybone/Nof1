import unittest, sys, os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from pipeline import *

from Nof1Pipeline.run_vep import RunVep

class TestBasic(unittest.TestCase):
    
    def setUp(self):
        print

    def test_vep(self):
    	in_fn='data/trip_neg_Vic/triple_negativ_mut_seq.vep'
        pipeline=Pipeline('mock', host, working_dir, True)
        bt2=RunVep(pipeline, in_fn)
        cmd=bt2.cmd_string()
	print cmd

        self.assertIn('perl', cmd)
        self.assertIn('variant_effect_predictor', cmd)
        self.assertIn(in_fn, cmd)
        self.assertIn('--format', cmd)
        self.assertIn('guess', cmd)
        self.assertIn('--cache', cmd)
	self.assertIn('-o', cmd)
	self.assertIn('vep.out', cmd) # replacement extension
	self.assertIn('--force_overwrite', cmd)

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBasic)
    unittest.TextTestRunner(verbosity=2).run(suite)



