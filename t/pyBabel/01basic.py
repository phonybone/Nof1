import unittest, sys, os, re
from warnings import warn

dir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..'))
sys.path.append(os.path.join(dir, 'lib'))
import pyBabel.Client as babel

class TestBasic(unittest.TestCase):
    
    def setUp(self):
        print
        
    def test_idtypes(self):
        client=babel.Client()
        typedict=client.getIDTypes()

        self.assertIn('gene_known', typedict)
        self.assertEqual(typedict['gene_known'], 'UCSC known gene id')

        self.assertIn('protein_ipi', typedict)
        self.assertEqual(typedict['protein_ipi'], 'IPI id')

        verbose=False
        if verbose:
            types=sorted(typedict.keys())
            for t in types:
                print t+'='+typedict[t]

    def test_translate_all(self):
        client=babel.Client()
        args={
            'input_type' : 'gene_known',
            'output_types' : ['gene_ensembl'],
            }
        table=client.translateAll(**args)
        print 'got %d translations' % len(table)

        # sends results back as a lol:
        for i in xrange(20):
            pair=table[i]
            print '%s -> %s' % (pair[0], pair[1])
        

    def test_translate(self):
        return
        client=babel.Client()
        args={
            'input_ids' : [],
            'input_type' : 'gene_known',
            'output_types' : [],
            'output_format' : 'json',
            }
        trans=client.translate(**args)
#-----------------------------------------------------------------------

suite = unittest.TestLoader().loadTestsFromTestCase(TestBasic)
def test_all():
    unittest.TextTestRunner(verbosity=2).run(suite)

if __name__ == "__main__":
    test_all()

