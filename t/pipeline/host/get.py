import unittest, sys, os, ConfigParser
from warnings import warn

dir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..'))
sys.path.append(os.path.join(dir, 'lib'))
from Pipeline.host import Host
config_file=os.path.join(os.path.join(dir, 'config', 'hosts.conf'))

class TestHost(unittest.TestCase):
    
    def setUp(self):
        print

    def test_localhost(self):
        try:
            host=Host(config_file, 'clutch')
        except Excption:
            self.fail('clutch not found')

        self.assertEquals(host.get('n_procs'), '2')

#-----------------------------------------------------------------------

suite = unittest.TestLoader().loadTestsFromTestCase(TestHost)
def test_all():
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
#    test_all()
    print 'fart'
    unittest.main()

