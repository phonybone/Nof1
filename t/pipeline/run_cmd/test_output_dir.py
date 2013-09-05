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
output_dir=os.path.dirname(__file__) or os.path.abspath('./outputs/test_output_dir')

class TestBasic(unittest.TestCase):
    
    def setUp(self):
        pass

    def test_output_dir(self):
        pipeline=Pipeline('mock', host, working_dir, output_dir=output_dir)
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


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBasic)
    unittest.TextTestRunner(verbosity=2).run(suite)

