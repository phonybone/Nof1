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
        pos2var=VariantPositions(self.variant_fn)
        self.stats.update(pos2var.stats)
        print
        self.count_variants(pos2var)
        self.consolidate_pos2var(pos2var)
        self.report(pos2var)
        return 0

                

    def count_variants(self, pos2var):
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
                    variant=pos2var.variant_for(line)
                    if not variant: continue
                    variant.n_alignments+=1
                    self.stats['n_variant_hits']+=1

                    if variant.is_expressed_in_seq(seq, pos):
                        variant.n_mut+=1
                    else:
                        variant.n_wt+=1
                    break



                

    def consolidate_pos2var(self, pos2var):
        sym2var={}
        for variant in pos2var.values():
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


    def report(self, pos2var):
#        for variant in pos2var.values():

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
