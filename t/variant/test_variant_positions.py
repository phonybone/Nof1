import unittest, sys, os
from warnings import warn

libdir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','lib'))
sys.path.append(libdir)
from variant_positions import VariantPositions

class TestReadVariantFile(unittest.TestCase):
    
    def setUp(self):
        print
        

    def test_read_variant_file(self):
        var_fn=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'fixtures', 'triple_negativ_mut_seq'))
        pos2var=VariantPositions(var_fn)
        stats=pos2var.stats

        self.assertEqual(stats['n_variants'], 1128)
        self.assertEqual(stats['n_snp'], 1022)
        self.assertEqual(stats['n_ins'], 1)
        self.assertEqual(stats['n_del'], 105)
        self.assertEqual(stats['n_ignored'], 264)
        self.assertEqual(stats['n_variant_errors'], 13)
        self.assertEqual(stats['n_genes'], 496)
        self.assertEqual(len(pos2var), 740)
        print stats

        # check that all variants bracket the alignments assigned to them:
        for k, var in pos2var.items():
            (chr, pos)=k.split('_')
            nchr=chr[3:]
            self.assertEqual(nchr, var.chrom)
            self.assertTrue(int(pos) >= int(var.start), '%s: %s <= %s' % (var, pos, var.start))
            self.assertTrue(int(pos) <= int(var.stop), '%s: %s >= %s' % (var, pos, var.stop))

#-----------------------------------------------------------------------

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestReadVariantFile)
    unittest.TextTestRunner(verbosity=2).run(suite)


