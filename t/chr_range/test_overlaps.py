import unittest, sys, os
from warnings import warn

libdir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','lib'))
sys.path.append(libdir)
from chr_range import ChrRange
from chrs import *

class TestEqOps(unittest.TestCase):
    def setUp(self):
        print
        
    def test_overlap(self):
        self.assertTrue(c11.overlaps(c11))

        self.assertTrue(c11.overlaps(c12))
        self.assertTrue(c12.overlaps(c12))

        self.assertTrue(c11.overlaps(c13))
        self.assertTrue(c13.overlaps(c11))

        self.assertTrue(c11.overlaps(c14))
        self.assertTrue(c14.overlaps(c11))

        self.assertTrue(c11.overlaps(c15))
        self.assertTrue(c15.overlaps(c11))

        self.assertTrue(c11.overlaps(c16))
        self.assertTrue(c16.overlaps(c11))

        self.assertTrue(c11.overlaps(c17))
        self.assertTrue(c17.overlaps(c11))

        self.assertFalse(c11.overlaps(c18))
        self.assertFalse(c11.overlaps(c18))


        self.assertFalse(c16.overlaps(c17))
        self.assertFalse(c17.overlaps(c16))

        self.assertFalse(c17.overlaps(c18))
        self.assertFalse(c18.overlaps(c17))

        self.assertFalse(c16.overlaps(c18))
        self.assertFalse(c18.overlaps(c16))

        
#-----------------------------------------------------------------------

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestEqOps)
    unittest.TextTestRunner(verbosity=2).run(suite)


