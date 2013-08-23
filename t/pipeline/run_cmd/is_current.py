import unittest, sys, os
d=os.path.abspath(os.path.join(os.path.dirname(__file__),'..', '..'))
sys.path.append(d)
from pipeline import *

from Pipeline.run_cmd import RunCmd
from Pipeline.Pipeline import Pipeline
from Pipeline.host import Host
from writer_cmd import writer_cmd

class MockCmd(RunCmd):
    def __init__(self, pipeline, skip_if_current=False):
        super(MockCmd,self).__init__('mock', pipeline, skip_if_current)
    def get_cmd(self): return 'echo'
    def get_args(self): return ['arg1', 'arg2']
    def inputs(self): return ['in1', 'in2']
    def outputs(self): return ['out1', 'out2']
        

class TestIsCurrent(unittest.TestCase):
    
    def setUp(self):
        pass

    def test_ins_younger_than_outs(self):
        pipeline=Pipeline('mock', host, working_dir, dry_run=True, echo=True)
        cmd=MockCmd('mock', pipeline)

        with open('in1', 'w') as i1: # open with 'w' to create if need be
            with open('in2', 'w') as i2:
                with open('out1', 'w') as o1:
                    with open('out2', 'w') as o2:
                        os.utime('in1', (10000,10000))
                        os.utime('in2', (10000,10000))
                        os.utime('out1', (20000,20000))
                        os.utime('out2', (20000,20000))
                        
                        self.assertTrue(cmd.is_current())

    def test_ins_older_than_outs(self):
        pipeline=Pipeline('mock', host, working_dir, dry_run=True, echo=True)
        cmd=MockCmd('mock', pipeline)

        with open('in1', 'w') as i1: # open with 'w' to create if need be
            with open('in2', 'w') as i2:
                with open('out1', 'w') as o1:
                    with open('out2', 'w') as o2:
                        os.utime('in1', (30000,30000))
                        os.utime('in2', (30000,30000))
                        os.utime('out1', (20000,20000))
                        os.utime('out2', (20000,20000))
                        
                        self.assertFalse(cmd.is_current())

    def test_missing_inputs(self):
        pipeline=Pipeline('mock', host, working_dir, dry_run=True, echo=True)
        cmd=MockCmd('mock', pipeline)

        try: os.unlink('in1')
        except OSError: pass
        try: os.unlink('in2')
        except OSError: pass
            
        with open('out1', 'w') as i1: # open with 'w' to create if need be
            with open('out2', 'w') as i2:
                os.utime('out1', (20000,20000))
                os.utime('out2', (20000,20000))
                
                self.assertFalse(cmd.is_current())


    def test_missing_outputs(self):
        pipeline=Pipeline('mock', host, working_dir, dry_run=True, echo=True)
        cmd=MockCmd('mock', pipeline)

        try: os.unlink('out1')
        except OSError: pass
        try: os.unlink('out2')
        except OSError: pass
            
        with open('in1', 'w') as i1: # open with 'w' to create if need be
            with open('in2', 'w') as i2:
                os.utime('in1', (20000,20000))
                os.utime('in2', (20000,20000))
                
                self.assertFalse(cmd.is_current())



    def test_one_in_younger_than_outs(self):
        pipeline=Pipeline('mock', host, working_dir, dry_run=True, echo=True)
        cmd=MockCmd('mock', pipeline)

        with open('in1', 'w') as i1: # open with 'w' to create if need be
            with open('in2', 'w') as i2:
                with open('out1', 'w') as o1:
                    with open('out2', 'w') as o2:
                        os.utime('in1', (30000,10000))
                        os.utime('in2', (10000,10000))
                        os.utime('out1', (20000,20000))
                        os.utime('out2', (25000,25000))
                        
                        self.assertTrue(cmd.is_current())





if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestIsCurrent)
    unittest.TextTestRunner(verbosity=2).run(suite)

