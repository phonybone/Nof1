import unittest, sys, os, re
from cStringIO import StringIO
from warnings import warn

root_dir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
sys.path.append(os.path.join(root_dir, 'lib'))

from Pipeline.Nof1Pipeline import Nof1Pipeline


from Pipeline.host import Host
host_conf=os.path.join(root_dir, 'config', 'hosts.conf')
host=Host(host_conf, 'clutch')
working_dir=os.path.join(root_dir, 'data')
output_dir=os.path.join(root_dir, 'outputs')

class TestBasic(unittest.TestCase):
    
    def setUp(self):
        host.set('dry_run', str(False))
        print

    def test_cmd(self):
        data_basename='test_rnaseq/rawdata/1047-COPD.1K'
        ref_index='hg19'
    	variants_fn='trip_neg_Vic/triple_negativ_mut_seq'

        Nof1Pipeline(host, working_dir, data_basename, ref_index, variants_fn,
                     output_dir=output_dir).run()
            

if __name__=='__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBasic)
    unittest.TextTestRunner(verbosity=2).run(suite)

