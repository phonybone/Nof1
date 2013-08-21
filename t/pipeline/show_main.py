import unittest, sys, os, re
from cStringIO import StringIO
from warnings import warn

root_dir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
sys.path.append(os.path.join(root_dir, 'lib'))

from Pipeline.MainPipeline import MainPipeline


from Pipeline.host import Host
host_conf=os.path.join(root_dir, 'config', 'hosts.conf')
host=Host(host_conf, 'clutch')
working_dir=os.path.join(root_dir, 'data')

class TestBasic(unittest.TestCase):
    
    def setUp(self):
        host.set('dry_run', str(True))
        print

    def test_cmd(self):
        data_basename='data/test_rnaseq/rawdata/1047-COPD.10K'
        ref_index='hg19'
    	variants_fn='data/trip_neg_Vic/triple_negativ_mut_seq'

        old_stdout=sys.stdout
        sys.stdout=mystdout=StringIO()
        
        MainPipeline(host, working_dir, data_basename, ref_index, variants_fn).run()
        sys.stdout=old_stdout
            
        lines=mystdout.getvalue().split('\n')
        for l in lines:
            print l

if __name__=='__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBasic)
    unittest.TextTestRunner(verbosity=2).run(suite)

