import unittest, sys, os
from warnings import warn

libdir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','lib'))
sys.path.append(libdir)
from variant import *

class TestExpressesSNP(unittest.TestCase):
    
    def setUp(self):
        print
        

    def test_expresses_del(self):
        var=Variant('ABC', 23, 'center', 'hg45', 'chr1', 3827, 3836, '+', 'Missense_Mutation', 'DEL', 
                    'GTATCCGTCA', 'GTATCCGTCA', '')
        seq='AAAAACCGAGCCCGGGGGTT'*4 # note presence of 'GAG' at correct location
        pos=3820                # has to encompass variant position of 3829
        self.assertTrue(var.is_expressed_in_seq(seq, pos))

        seq='AAAAACGGTATCCGTCAAGC'*4 # note presence of 'GAG' at incorrect location
        self.assertFalse(var.is_expressed_in_seq(seq, pos))


#-----------------------------------------------------------------------

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestExpressesSNP)
    unittest.TextTestRunner(verbosity=2).run(suite)


