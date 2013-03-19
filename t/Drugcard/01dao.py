import unittest, sys, os
from warnings import warn

libdir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
sys.path.append(os.path.join(libdir, 'lib'))
from drugcard import Drugcard
from drugbank_reader import DrugbankReader
from dao_mongo import dao_mongo
from dump_obj import dump

class TestDao(unittest.TestCase):
    
    def setUp(self):
        self.dc_dao=dao_mongo(cls=Drugcard, db='test_nof1')
        self.dc_dao.remove()
        
    def test_dao(self):
        fn=os.path.join(libdir, 'data', 'drugbank.2.txt')
        reader=DrugbankReader(fn)
        dc_dao=self.dc_dao
        for dc in reader.iter():
            print '%s: %d targets' % (dc.id, len(dc.targets))
            dc_dao.save(dc)

        dc1=dc_dao.find_first({'id':'DB00001'})
        self.assertEquals(dc1.id,'DB00001')
        self.assertEquals(dc1.AHFS_Codes, [u'20:12.04.12'])
        print 'dc1: %d targets' % len(dc1.targets)
        self.assertEquals(len(dc1.targets), 1)

        t1=dc1.targets[0]
        print 't1.Pathway[0]: %s' % t1.Pathway[0]
        self.assertEquals(t1.Pathway[0], 'Abciximab Pathway	SMP00265')

        dc2=dc_dao.find_first({'id':'DB00002'})
        self.assertEquals(dc2.id,'DB00002')
        self.assertEquals(dc2.AHFS_Codes, [u'Not Available'])
        print 'dc2: %d targets' % len(dc2.targets)
        self.assertEquals(len(dc2.targets), 12)

        


#-----------------------------------------------------------------------

suite = unittest.TestLoader().loadTestsFromTestCase(TestDao)
def test_all():
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
    test_all()

