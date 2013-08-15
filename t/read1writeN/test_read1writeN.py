import unittest, sys, os, csv
from warnings import warn

libdir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','lib'))
sys.path.append(libdir)
from read1writeN import Read1WriteN

class TestSomething(unittest.TestCase):
    outs={'red':'red.txt',
          'orange':'orange.txt',
          'yellow':'yellow.txt',
          'green':'green.txt',
          'blue':'blue.txt',
          'purple':'purple.txt'}
        
    
    def setUp(self):
        for fn in self.outs.values():
            try: os.unlink(fn)
            except OSError: pass
        print
        
    def tearDown(self):
        for fn in self.outs.values():
            try: os.unlink(fn)
            except OSError: pass

    def test_something(self):
        
        # split colors.txt on each line:
        fodder_fn=os.path.join(os.path.dirname(__file__), 'colors.txt')
        print 'fodder_fn is %s' % fodder_fn
        with Read1WriteN(fodder_fn,**self.outs) as splitter:
            with open(splitter.rn1) as f:
                for line in f.readlines():
                    color=line.strip()
                    f=splitter.k2f[color]
                    f.write('%s\n' % color)

        # assert that each generated file only contains its color:
        for color, fn in self.outs.items():
            with open(fn) as f:
                for l in f.readlines():
                    self.assertEqual(l.strip(), color)


#-----------------------------------------------------------------------

suite = unittest.TestLoader().loadTestsFromTestCase(TestSomething)
def test_all():
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
    test_all()

