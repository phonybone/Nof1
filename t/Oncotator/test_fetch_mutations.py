import unittest, sys, os
from warnings import warn

dir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','lib'))
sys.path.append(dir)
from oncotator import Oncotator

class TestMutationInfo(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def test_mutation_info(self):
        o=Oncotator()
        mutations='''
7  55259515  55259515  T  G
7 140453136 140453136 A T
1  120612003  120612004  GG  -
8  145138175  145138176  -  G
12  42538391  42538401  GGAGCGAGCAG  -
'''
        info=o.fetch_mutation_info(mutations)
        print info

#-----------------------------------------------------------------------

suite = unittest.TestLoader().loadTestsFromTestCase(TestMutationInfo)
def test_all():
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
    test_all()

