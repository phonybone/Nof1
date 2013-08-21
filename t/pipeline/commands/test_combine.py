import unittest, sys, os, re
from warnings import warn

root_dir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..'))
sys.path.append(os.path.join(root_dir, 'lib'))
from Pipeline.run_combine import RunCombine
from Pipeline.Pipeline import Pipeline
from Pipeline.host import Host
host_conf=os.path.join(root_dir, 'config', 'hosts.conf')
host=Host(host_conf, 'clutch')
working_dir=os.path.join(root_dir, 'data')

class TestBasic(unittest.TestCase):
    
    def setUp(self):
        print

    def test_combine(self):
        pipeline=Pipeline('mock', host, working_dir, True)
        data_basename='1047-COPD.10K'
        variants_fn='triple_negativ_mut_seq'
        gene_counts_fn=os.path.join(root_dir, 't', 'fixtures', '%s.genes.count' % data_basename)
        auto_fn=os.path.join(root_dir, 't', 'fixtures', '%s.auto' % variants_fn)
        vep_filter_fn=os.path.join(root_dir, 't', 'fixtures', '%s.vep.filtered' % variants_fn)
        comb=RunCombine(pipeline, gene_counts_fn, auto_fn, vep_filter_fn)
        cmd=comb.cmd_string()
#        print cmd

        self.assertIn(host.get('combine.script'), cmd)
        self.assertIn(data_basename, cmd)
        self.assertIn(variants_fn, cmd)



if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBasic)
    unittest.TextTestRunner(verbosity=2).run(suite)

