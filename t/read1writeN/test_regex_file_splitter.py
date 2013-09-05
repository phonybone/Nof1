import unittest, sys, os, csv
from warnings import warn

libdir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','lib'))
sys.path.append(libdir)
from regex_file_splitter import RegexFileSplitter

class TestSomething(unittest.TestCase):
    outs=[['red','red.txt'],
          ['orange','orange.txt'],
          ['yellow','yellow.txt'],
          ['green','green.txt'],
          ['blue','blue.txt'],
          ['purple','purple.txt']]
        
    
    def setUp(self):
        for fn in [x[1] for x in self.outs]:
            try: os.unlink(fn)
            except OSError: pass
        print
        
    def tearDown(self):
        for fn in [x[1] for x in self.outs]:
            try: os.unlink(fn)
            except OSError: pass

    def test_colors(self):
        # split colors.txt on each line:
        fodder_fn=os.path.join(os.path.dirname(__file__), 'colors.txt')
        splitter=RegexFileSplitter(fodder_fn, *self.outs)
        splitter.split()
     
        # assert that each generated file only contains its color:
        for pair in self.outs:
            (color, fn)=(pair[0], pair[1])
            with open(fn) as f:
                for l in f.readlines():
                    self.assertEqual(l.strip(), color)


#-----------------------------------------------------------------------

suite = unittest.TestLoader().loadTestsFromTestCase(TestSomething)
def test_all():
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
    test_all()

