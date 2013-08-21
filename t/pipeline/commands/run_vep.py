import unittest, sys, os
from warnings import warn

root_dir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..'))
sys.path.append(os.path.join(root_dir, 'lib'))
from Pipeline.run_vep import RunVep
from Pipeline.Pipeline import Pipeline
sys.path.append(os.path.join(root_dir, 't', 'pipeline'))

from Pipeline.host import Host
host_conf=os.path.join(root_dir, 'config', 'hosts.conf')
host=Host(host_conf, 'clutch')
working_dir=os.path.join(root_dir, 'data')

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



