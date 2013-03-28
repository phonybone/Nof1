import unittest, sys, os
from warnings import warn

dir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','lib'))
sys.path.append(dir)
from ttd_builder_factory import TtdBuilderFactory

class TestTtdbuilderfactory(unittest.TestCase):
    
    def setUp(self):
        pass
        
    def test_ttdbuilderfactory(self):
        f=TtdBuilderFactory()
        self.assertEquals(f.get_instance('rdf').__class__.__name__,'TtdBuilderRdf')
        self.assertEquals(f.get_instance('sqlite').__class__.__name__,'TtdBuilderSqlite')

#-----------------------------------------------------------------------

suite = unittest.TestLoader().loadTestsFromTestCase(TestTtdbuilderfactory)
def test_all():
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
    test_all()

