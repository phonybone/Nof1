import unittest, sys, os
from warnings import warn

libdir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','lib'))
sys.path.append(libdir)
from chr_range import ChrRange
from chrs import *

class TestEqOps(unittest.TestCase):

    def setUp(self):
        print
        
    def test_equals(self):
        self.assertEqual(c11, c12)
        self.assertNotEqual(c11, c21)
        self.assertNotEqual(c11, c13)
        self.assertNotEqual(c11, c14)        
        self.assertNotEqual(c11, c15)        

    def test_equals_subclass(self):
        class ChrRange2(ChrRange): pass
        c2=ChrRange2('chr1', 10, 20)
        self.assertEqual(c11, c2)
        self.assertEqual(c2, c11)

    def test_gt(self):
        self.assertTrue(c11 < c16)
        self.assertTrue(c11 <= c16)
        self.assertTrue(c11 != c16)
        self.assertTrue(c16 > c11)
        self.assertTrue(c16 >= c11)

        self.assertFalse(c11 < c14)
        self.assertTrue(c11 <= c14)
        self.assertTrue(c11 != c14)
        self.assertTrue(c14 > c11)
        self.assertTrue(c14 >= c11)

        
        
#-----------------------------------------------------------------------

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEqOps)
    unittest.TextTestRunner(verbosity=2).run(suite)


