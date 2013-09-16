import sys, os

'''
Split an rnaseq file according to which variant a read lands on.
Used for creating smaller read sets for debugging purposes.
'''

libdir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','lib'))
sys.path.append(libdir)
from nof1_args import Nof1Args
from variant_positions import VariantPositions
from progress_dots import ProgressDots

def main(args):
    if args.v: print args
    print 'reading %s...' % args.variant_fn
    pos2var=VariantPositions(args.variant_fn)

    try: os.mkdir(args.output_dir)
    except OSError: pass

    for f in os.listdir(args.output_dir):
        os.unlink(os.path.join(args.output_dir, f))

    dots=ProgressDots(args.dot_counter)

    stats={'n_reads':0,
           'n_variants':0}
    print 'reading %s...' % args.rnaseq_fn
    with open(args.rnaseq_fn) as f:
        for line in f:
            dots.ping()
            if line.startswith('@'):
                continue
            stats['n_reads']+=1

            row=line.split('\t')
            var=pos2var.variant_for(row[2], int(row[3]), len(row[9]))
            if not var: continue
            stats['n_variants']+=1
            try:
                var.reads.append(line)
            except AttributeError:
                var.reads=[line]
    print

    # write out all reads for each variant:
    for var in pos2var.values():
        try:
            fn=os.path.join(args.output_dir, '%s.fastq' % var.symbol)
            with open(fn, 'w') as var_f:
                for line in var.reads:
                    var_f.write(line)
        except AttributeError:  # on var.reads
            pass

    print stats
    return 0


if __name__=='__main__':
    config_fn=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'nof1.conf'))
    args=Nof1Args(config_fn, 'split rnaseq reads according to variant', 'variant_splitter')
    sys.exit(main(args.args))
