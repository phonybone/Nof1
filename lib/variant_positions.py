import csv
from variant import Variant, VariantError

class VariantPositions(dict):
    '''
    Read a variant file (eg triple_negativ_mut_seq).
    Construct a dict w/key = 'chr%s_%d', where %d is a genomic coord
                     w/value = Variant(f.readline()).

    The purpose of this class is to allow rapid id of aligned reads to variants.

    There will be one entry in the dict for each position of the variant, so
    if the variant has len==4, there will be 4 entries in the dict for that variant.
    There may also be more than one variant/gene.
    This is done so that reads that start at any point of the variant may be found.
    '''

    def __init__(self, variant_fn, verbose=False):
        self.variant_fn=variant_fn
        self.verbose=verbose
        self.stats=self.read_variant_file()

    def read_variant_file(self):
        '''
        Read in the variant file, store to dict "pos2var"
        k is "chr%s_%d" % (variant.start, i) where i is each position on the chromosome 
        that the variant occupies.  v is the variant.
        '''

        stats={
            'n_variants':0,
            'n_snp':0,
            'n_ins':0,
            'n_del':0,
            'n_variant_errors':0,
            'n_ignored':0,
        }

        gene_symbols={}

        with open(self.variant_fn) as vf:
            reader=csv.reader(vf, delimiter='\t')
            for line in reader:
                if line[0].startswith('#'): continue
                (symbol, entrez, center, build, chrom, start, stop, strand, var_class, var_type, ref_allele, tum_seq1, tum_seq2)=line[:13]

                try:
                    variant=Variant(symbol, entrez, center, build, chrom, start, stop, strand, var_class, var_type, ref_allele, tum_seq1, tum_seq2)
                    stats['n_'+var_type.lower()]+=1
                    
                    try: gene_symbols[symbol]+=1
                    except KeyError: gene_symbols[symbol]=1

                except ValueError: # happens for comment lines, etc
                    continue

                except VariantError, e:
                    if self.verbose: 
                        print e
                    stats['n_variant_errors']+=1
                    continue
                
                stats['n_variants']+=1
                if variant.ref_type == 'ignore':
                    stats['n_ignored']+=1
                    continue

                # make a hash entry for each possible variant location:
                for i in range(variant.start, variant.stop+1):
                    key='chr%s_%d' % (variant.chrom, i)

                    #print 'adding %s->%s: chr%s:%d-%d (%d)' % (key, variant.symbol, variant.chrom, variant.start, variant.stop, variant.stop-variant.start+1)

                    self[key]=variant

        stats['n_genes']=len(gene_symbols)
        try:
            stats['ratio_genes_variants']=float(stats['n_genes'])/stats['n_variants']
        except ZeroDivisionError:
            stats['ratio_genes_variants']=None
        return stats

    def variant_for(self, chrom, pos, length):
        for i in range(length):
            key='%s_%d' % (chrom, pos+i)
            if key in self:
                return self[key]
        return None


