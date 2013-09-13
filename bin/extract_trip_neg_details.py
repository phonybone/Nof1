import sys, os, re, csv, traceback
libdir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','lib'))
sys.path.append(libdir)

from nof1_args import Nof1Args
from read1write2 import read1write2


ref_types={
    'Frame_Shift_Del':   'auto',
    'Frame_Shift_Ins':   'auto',
    'In_Frame_Del':      'polyphen',
    'In_Frame_Ins':      'polyphen',
    'Missense_Mutation': 'polyphen',
    'Nonsense_Mutation': 'auto',
    'RNA':               'ignore',
    'Silent':            'ignore',
    'Splice_Site':       'auto'
} 
    


def main(nof1_args):
    '''
    convert data/trip_neg_Vic/triple_mut_seq into a format that the Ensembl VEP can use.
    input: raw mutations file (eg triple_negativ_mut_seq
    outputs:
      - file suitable for feeding to vep.pl script
      - file of auto-selected mutations taken verbatim from input file (see ref_types w/value='auto')
    '''
    args=nof1_args.args
    if args.v: print args
    
    stats={'n_auto':0,
           'n_ignored':0,
           'n_polyphen':0,
           'n_unknown':0,
           'n_total':0,
           }
    

    in_fn=args.in_fn
    if not in_fn:                  # argparse doesn't require it
        nof1_args.parser.print_help()
        sys.exit(1)

    poly_fn=args.poly_fn
    auto_fn=args.auto_fn


    with read1write2(in_fn, poly_fn, auto_fn) as f3:
        reader=csv.reader(f3.r1, delimiter='\t')
        for line in reader:
            try:
                sym=line[0]
                chrm=line[4]
                start=line[5]
                try:
                    istart=int(start) # not used; just weeds out bad lines
                except:
                    if args.v:
                        sys.stderr.write("can't convert %s to int\n" % start)
                    continue

                stats['n_total']+=1
                (stop, strand, var_class, var_type, ref, a1, t1, t2)=line[6:14]
                try:
                    ref_type=ref_types[var_class]
                except KeyError:
                    stats['n_unknown']+=1
                    continue

                if ref_type=='ignore':
                    stats['n_ignored']+=1
                    continue
                elif ref_type=='auto':
                    f3.w2.write('\t'.join(line)+'\n')
                    stats['n_auto']+=1
                    continue

                if a1 != ref:   # a1 and a2 are reference alleles
                    f3.w1.write('%s %s %s %s/%s %s %s\n' % (chrm, start, stop, ref, a1, strand, sym))
                if t1 != ref:
                    f3.w1.write('%s %s %s %s/%s %s %s\n' % (chrm, start, stop, ref, t1, strand, sym))
                
                stats['n_polyphen']+=1

            except Exception, e:
                print 'caught %s' % e
                print '\t'.join(line)
                traceback.print_exc()
                print

    print '%s' % stats

if __name__=='__main__':
    config_fn=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'nof1.conf'))
    args=Nof1Args(config_fn, 'extract the fields from the trip_neg_details_6cases.txt file (or similar)', 'extract_trip_neg_details')
    main(args)

