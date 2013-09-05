import unittest, sys, os
from warnings import warn

libdir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','lib'))
sys.path.append(libdir)
from chr_range import *

class TestChrRange(unittest.TestCase):
    
    def setUp(self):
        print
        
    def test_good_constructors(self):
        c=ChrRange('chr1', 4, 8)
        self.assertEqual(str(c), 'chr1: 4 8')

        c=ChrRange('chr3', 14, 87)
        self.assertEqual(str(c), 'chr3: 14 87')

        c=ChrRange('chr23', 4, 8)
        self.assertEqual(str(c), 'chr23: 4 8')

        c=ChrRange('chrX', 4, 8)
        self.assertEqual(str(c), 'chrx: 4 8')

    def test_bad_constructors(self):
        with self.assertRaises(ChrIndexError) as cm:
            ChrRange('chr3', 10, 5)
        self.assertEqual(str(cm.exception), 'chr3: 10 5: start > stop')

        with self.assertRaises(ChrException) as cm:
            ChrRange('fred', 10, 5)
        print cm.exception

        with self.assertRaises(ChrIndexError) as cm:
            ChrRange('chr45', 48, 90)
        print cm.exception

        with self.assertRaises(ChrIndexError) as cm:
            ChrRange('chr_seven', 48, 90)
        print cm.exception

        

#-----------------------------------------------------------------------

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestChrRange)
    unittest.TextTestRunner(verbosity=2).run(suite)


