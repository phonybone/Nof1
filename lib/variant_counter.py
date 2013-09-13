import sys, csv
from variant import Variant, VariantError
from progress_dots import ProgressDots

class VariantCounter(object):
    '''
    
    '''

    def __init__(self, args):
        self.args=args
        self.variant_fn=args.variant_fn
        self.rnaseq_fn=args.rnaseq_fn
        self.stats={'n_variants':0,
                    'n_alignments':0,
                    'n_variant_hits':0,
                    'n_variant_errors':0,
                    'n_snp':0,
                    'n_ins':0,
                    'n_del':0,
                    'n_ignored':0,
        }

    def go(self):
        self.pos2var=self.read_variant_file()
        print
        self.count_variants()
        self.consolidate_pos2var()
        self.report()
        return 0

    def read_variant_file(self):
        '''
        Read in the variant file, store to dict "pos2var"
        k is "chr%s_%d" % (variant.start, i) where i is each position on the chromosome 
        that the variant occupies.  v is the variant.
        '''
        pos2var={}

        with open(self.variant_fn) as vf:
            reader=csv.reader(vf, delimiter='\t')
            for line in reader:
                if line[0].startswith('#'): continue
                (symbol, entrez, center, build, chrom, start, stop, strand, var_class, var_type, ref_allele, tum_seq1, tum_seq2)=line[:13]

                # fixme: filter on var_type (or var_class??)

                try:
                    variant=Variant(symbol, entrez, center, build, chrom, start, stop, strand, var_class, var_type, ref_allele, tum_seq1, tum_seq2)
                    self.stats['n_'+var_type.lower()]+=1
                except ValueError:
                    continue
                except VariantError, e:
                    if self.args.v: 
                        print e
                    self.stats['n_variant_errors']+=1
                    continue
                
                self.stats['n_variants']+=1
                if variant.ref_type == 'ignore':
                    self.stats['n_ignored']+=1
                    continue

                # make a hash entry for each possible variant location:
                # print 'adding %s: chr%s:%d-%d (%d)' % (variant.symbol, variant.chrom, variant.start, variant.stop, variant.stop-variant.start+1)
                for i in range(variant.start, variant.stop+1):
                    key='chr%s_%d' % (variant.chrom, i)
                    pos2var[key]=variant
        return pos2var
                

    def count_variants(self):
        dots=ProgressDots(self.args.dot_counter)

        with open(self.rnaseq_fn) as rf:
            reader=csv.reader(rf, delimiter='\t')
            for line in reader:
                if line[0].startswith('@'): continue
                chrom=line[2]
                pos=int(line[3])
                seq=line[9]
                # print 'alignment: %s %d-%d (%d) %s' % (chrom, pos, pos+len(seq), len(seq), seq)

                self.stats['n_alignments']+=1
                if self.args.progress: dots.ping()

                # crawl the aligned read, looking for a variant:
                # This is O(m*n) on the number and length of the reads,
                # but it's O(1) for programmer laziness.
                for i in range(len(seq)):
                    key='%s_%d' % (chrom, pos+i)
                    if key in self.pos2var:
                        variant=self.pos2var[key]
                        variant.n_alignments+=1

                        # do something here about figuring out which allele is represented
                        if self.args.v:
                            print 'alignment: %s (pos=%d, strand=%s)' % (seq, pos, variant.strand)
                            print 'overlaps with variant: %s, chr=%s, %d-%d\n' % (variant.symbol, 
                                                                                  variant.chrom,
                                                                                  variant.start,
                                                                                  variant.stop)
                        
                        self.stats['n_variant_hits']+=1
                        if variant.is_expressed_in_seq(seq, pos):
                            variant.n_mut+=1
                        else:
                            variant.n_wt+=1

                        break


                

    def consolidate_pos2var(self):
        sym2var={}
        for variant in self.pos2var.values():
            try:
                var=sym2var[variant.symbol]
                var.n_alignments+=variant.n_alignments
                var.n_wt+=variant.n_wt
                var.n_mut+=variant.n_mut
                var.n_spans+=1

            except KeyError:
                sym2var[variant.symbol]=variant
                variant.n_spans+=1
            
        self.sym2var=sym2var


    def report(self):
#        for variant in self.pos2var.values():

        row='\t'.join(['symbol', 'chrom', 'start', 'stop', 'strand',
                       'n_align', 'n_wt', 'n_mut', 'ratio', 'n_spans'])
        print '# %s' % row

        for key in sorted(self.sym2var.keys()):
            variant=self.sym2var[key]
            if variant.reported: continue
            variant.reported=True

            if variant.n_alignments != 0:
                ratio='%5.3f' % (float(variant.n_wt)/float(variant.n_alignments))
            else:
                ratio=None

            row='\t'.join([str(x) for x in [variant.symbol, 
                                            variant.chrom, variant.start, variant.stop, 
                                            variant.strand,
                                            variant.n_alignments, variant.n_wt, variant.n_mut, 
                                            ratio, variant.n_spans]])
            print row

        # print stats
        for k,v in self.stats.items():
            print '%s: %d' % (k,v)
