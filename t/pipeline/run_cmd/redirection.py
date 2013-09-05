import unittest, sys, os, re
from warnings import warn

root_dir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..'))
sys.path.append(os.path.join(root_dir, 'lib'))
from Pipeline.run_cmd import RunCmd
from Pipeline.Pipeline import Pipeline
from Pipeline.host import Host
from writer_cmd import writer_cmd

host_conf=os.path.join(root_dir, 'config', 'hosts.conf')
host=Host(host_conf, 'clutch')
working_dir=os.path.dirname(__file__) or os.path.abspath('.')

class TestBasic(unittest.TestCase):
    
    def setUp(self):
        pass

    def test_simplest(self):
        pipeline=Pipeline('mock', host, working_dir)
        cmd=writer_cmd('writer', pipeline)
        cmd.run()

        with open(cmd._get_stdout()) as f:
            contents=f.read()
            expected='this goes to stdout\n'
            self.assertEqual(contents, expected)

        with open(cmd._get_stderr()) as f:
            contents=f.read()
            expected='this goes to stderr\n'
            self.assertEqual(contents, expected)

        os.unlink(cmd._get_stdout())
        os.unlink(cmd._get_stderr())


    def _test_bowtie2(self):
        pipeline=Pipeline('mock', host, working_dir)
        data_basename='1047-COPD.10K'
        ref_index='hg19'
        bt2=RunBowtie2(pipeline, data_basename, ref_index)
        bt2.run()

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBasic)
    unittest.TextTestRunner(verbosity=2).run(suite)

