import unittest, sys, os, re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from pipeline import *

from Nof1Pipeline.run_find_common import RunFindCommon

class TestBasic(unittest.TestCase):
    
    def setUp(self):
        print

    def test_find_common(self):
        arg1={'fn':'test_rnaseq/rawdata/1047-COPD.10K.genes.count',
              'alias':'rnaseq',
              'field_no':1,
              'delimiter':':'}
 
        arg2={'fn':'trip_neg_Vic/triple_negativ_mut_seq.vep.out',
              'alias':'vep',
              'field_no':4}

 
        out_fn=os.path.join(working_dir, '1047-COPD_triple_negativ_mut_seq.common')
        expected='%s --out_fn %s test_rnaseq/rawdata/1047-COPD.10K.genes.count,rnaseq,1,: trip_neg_Vic/triple_negativ_mut_seq.vep.out,vep,4' % (host.get('find_common.script'), out_fn)

        pipeline=Pipeline('mock', host, working_dir, True)
        fc=RunFindCommon(pipeline, [arg1, arg2])
        cmd=fc.cmd_string()
        self.assertEqual(cmd, expected, '\ncmd:      %s\nexpected: %s' % (cmd, expected))


        

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBasic)
    unittest.TextTestRunner(verbosity=2).run(suite)

