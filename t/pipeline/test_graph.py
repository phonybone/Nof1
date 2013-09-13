import unittest, sys, os, argparse
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from pipeline import *
from Nof1Pipeline.Nof1Pipeline import Nof1Pipeline
from Pipeline.exceptions import *
import networkx as nx

class TestGraph(unittest.TestCase):
    
    def setUp(self):
#        host.set('dry_run', str(False))
        print

    def test_graph(self):
        data_basename='test_rnaseq/rawdata/1047-COPD.1K2'
        ref_index='hg19'
    	variants_fn='trip_neg_Vic/triple_negativ_mut_seq'

        p=Nof1Pipeline(host, working_dir, data_basename, ref_index, variants_fn,
                       output_dir=output_dir, 
                       dry_run=args.dry_run,
                       echo=not args.no_echo, 
                       skip_if_current=args.skip)

        g=p.graph()
        for n1,n2,d in g.edges_iter(data=True):
            print 'edge %-30s %-30s %s' % (n1, d['type'], n2)
        
        self.assertEqual(p.find_command('vep').inputs()[0], 'trip_neg_Vic/triple_negativ_mut_seq.poly')
        self.assertEqual(p.find_command('vep').outputs()[0], 'trip_neg_Vic/triple_negativ_mut_seq.vep.out')

        try:
            self.assertTrue(p.check_continuity())
        except ContinuityError:
            self.fail()

            

if __name__=='__main__':
    parser=argparse.ArgumentParser(description='run pipeline harness')
    parser.add_argument('--dry_run', default=False, action='store_true')
    parser.add_argument('--no_echo', default=False, action='store_true')
    parser.add_argument('--skip', default=False, action='store_true')
    args=parser.parse_args()
    print args

    suite = unittest.TestLoader().loadTestsFromTestCase(TestGraph)
    unittest.TextTestRunner(verbosity=2).run(suite)

