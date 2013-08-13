import unittest, sys, os, ConfigParser
from socket import gethostname
from warnings import warn

dir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..'))
sys.path.append(os.path.join(dir, 'lib'))
from Pipeline.host import Host

config_file=os.path.join(os.path.join(dir, 'config', 'hosts.conf'))

class TestHost(unittest.TestCase):
    
    def setUp(self):
        print

    def test_localhost(self):
        # create temp hosts.conf
        import tempfile
        with tempfile.NamedTemporaryFile() as tf:
            hostname=gethostname()
            contents= \
'''[%s]
this: that
''' % hostname
            tf.write(contents)
            tf.flush()

            # create section with name of local host, populate with random values
            try:
                host=Host(tf.name)
            except Exception, e:
                self.fail('localhost not found: %s' % e)

        

    def test_remote_host(self):
        try:
            host=Host(config_file, 'buffy')
        except Exception:
            self.fail('host buffy not found')

    def test_unknown_host(self):
        with self.assertRaises(ConfigParser.NoSectionError):
            host=Host(config_file, 'no_such_host')
            

#-----------------------------------------------------------------------

suite = unittest.TestLoader().loadTestsFromTestCase(TestHost)
#def test_all():
#    print 'hey you!'
unittest.TextTestRunner(verbosity=2).run(suite)

#if __name__ == "__main__":
#test_all()

