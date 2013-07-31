import unittest, sys, os, re, ConfigParser
from warnings import warn

dir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
sys.path.append(os.path.join(dir, 'lib'))
from Nof1.Pipeline.run_vep import RunVep

class TestBasic(unittest.TestCase):
    conf=ConfigParser.ConfigParser()
    fn=os.path.join(dir, 'config', 'hosts.conf')
    conf.read(fn)
    
    def setUp(self):
        print

    def test_cmd(self):
    	in_fn='data/trip_neg_Vic/triple_negativ_mut_seq.vep'
        bt2=RunVep(in_fn, self.conf)
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

suite = unittest.TestLoader().loadTestsFromTestCase(TestBasic)
def test_all():
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
    test_all()

