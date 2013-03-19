import unittest, sys, os, re
from warnings import warn

dir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
sys.path.append(os.path.join(dir, 'lib'))
from drugbank_reader import DrugbankReader
from drugcard_builder_rdf import DrugcardBuilderRdf

class TestDcb_Rdf(unittest.TestCase):
    
    def setUp(self):
        print
        
    def test_dcb_rdf(self):
        reader=DrugbankReader(builder=DrugcardBuilderRdf(), 
                              fn=os.path.join(dir, 't', 'drugbank.2.txt'))
        i=reader.__iter__()
        dc=i.next()
        print 'dc: id=%s' % dc.id
        self.assertTrue(re.search('DB00001', dc.id))
        self.assertEquals(len(dc.targets), 1)
        self.assertEquals(len(dc.seqs.keys()), 1)
        
        dc2=i.next()
        print 'got dc=%s' % dc


        for dc in reader:
            print '2nd: id=%s' % dc.id

#-----------------------------------------------------------------------

suite = unittest.TestLoader().loadTestsFromTestCase(TestDcb_Rdf)
def test_all():
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
    test_all()

