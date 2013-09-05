import unittest, sys, os, re
from warnings import warn

libdir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
sys.path.append(os.path.join(libdir, 'lib'))
from pyBabel.SmartClient import SmartClient

class TestBasic(unittest.TestCase):
    
    def setUp(self):
        print

    def test_ens2sym(self):
        client=SmartClient()
        id_types=['gene_ensembl','gene_symbol']
        key='2'.join(id_types)

        cache_path=client._get_cache_path(id_types)
        print 'deleting %s' % cache_path
        try: os.unlink(cache_path)
        except OSError: pass

        client.load(id_types)

        self.assertTrue(os.path.exists(cache_path)) # newly created
        self.assertIn(key, client.tables, 'no %s in tables' % key)
        self.assertTrue(hasattr(client, key))
        f=getattr(client,key)
        self.assertTrue(callable(f), 'client.%s not callable (%s)' % (key, type(f)))

        self.assertTrue(hasattr(client, 'tables'), 'client has no attr "tables"')
        self.assertEqual(type(getattr(client, 'tables')), type({}))
        self.assertEqual(client.gene_ensembl2gene_symbol('ENSG00000011021'),'CLCN6')
        
#-----------------------------------------------------------------------


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestBasic)
    unittest.TextTestRunner(verbosity=2).run(suite)


