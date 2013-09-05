import csv
from variant import Variant

class VariantCounter(object):
    def __init__(self, args):
        self.variant_fn=args.variant_fn
        self.rnaseq_fn=args.rnaseq_fn
        self.stats={'n_variants':0,
                    'n_alignments':0,
                    'n_variant_hits':0}

    def go(self):
        self.var2info=self.read_var_file()
        self.count_variants()
        self.report()
        return 0

    def read_var_file(self):
        var2info={}
        with open(self.variant_fn) as vf:
            reader=csv.reader(vf, delimiter='\t')
            for line in reader:
                if line[0].startswith('#'): continue
                (symbol, entrez, center, build, chrom, start, stop, strand, var_class, var_type, ref_allele, tum_seq1, tum_seq2)=line[:13]
                try:
                    variant=Variant(symbol, entrez, center, build, chrom, start, stop, strand, var_class, var_type, ref_allele, tum_seq1, tum_seq2)
                except ValueError:
                    continue
                self.stats['n_variants']+=1


                # make a hash entry for each possible variant location:
                for i in range(variant.start, variant.stop+1):
                    key='%s_%d' % (variant.chrom, i)
                    var2info[key]=variant
        return var2info
                

    def count_variants(self):
        with open(self.rnaseq_fn) as rf:
            reader=csv.reader(rf, delimiter='\t')
            for line in reader:
                if line[0].startswith('@'): continue
                chrom=line[2]
                pos=int(line[3])
                seq=line[8]
                self.stats['n_alignments']+=1

                # crawl the aligned read, looking for a variant:
                for i in range(len(seq)):
                    try:
                        key='%s_%d' % (chrom, pos+i)
                        variant=self.var2info[key]
                        variant.alignments+=1

                        # do something here about figuring out which allele is represented
                        print 'alignment: %s' % seq
                        print 'overlaps with variant: %s, chr=%s, %d-%d' % (variant.symbol, 
                                                                            variant.chrom,
                                                                            variant.start,
                                                                            variant.stop)
                        self.stats['n_variant_hits']+=1
                        break
                    except KeyError:
                        continue 

                


    def report(self):
        for k,v in self.stats.items():
            print '%s: %d' % (k,v)
