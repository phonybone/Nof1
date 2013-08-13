import sys, os, re, csv, traceback
libdir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','lib'))
sys.path.append(libdir)

from nof1_args import Nof1Args

def main(nof1_args):
    '''
    convert data/trip_neg_Vic/triple_mut_seq into a format that the Ensembl VEP can use.
    '''
    args=nof1_args.args
#    print args
    
    stats={'n_vars':0}
    keep_refs=['Frame_Shift_Del',
               'Frame_Shift_Ins',
               'In_Frame_Del',
               'In_Frame_Ins',
               'Missense_Mutation',
#               'Nonsense_Mutation',
#               'RNA',
#               'Silent',
               'Splice_Site']

    fn=args.in_fn
    if not fn:
        nof1_args.parser.print_help()
        sys.exit(1)

    with open(fn) as f:
        reader=csv.reader(f, delimiter='\t')
        for line in reader:
            try:
                sym=line[0]
                chrm=line[4]
                start=line[5]
                try:
                    istart=int(start) # not used; just weeds out bad lines
                except:
                    sys.stderr.write("can't convert %s to int\n" % start)
                    continue

                (stop, strand, t1, t2, ref, a1, a2)=line[6:12]
                if ref not in keep_refs: 
                if a1 != ref:   # a1 and a2 are reference alleles
                    print '%s %s %s %s/%s %s %s' % (chrm, start, stop, ref, a1, strand, sym)
                if a2 != ref:
                    print '%s %s %s %s/%s %s %s' % (chrm, start, stop, ref, a2, strand, sym)
                
            except Exception, e:
                print 'caught %s' % e
                traceback.print_exc()


if __name__=='__main__':
    config_fn=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'nof1.conf'))
    args=Nof1Args(config_fn, 'extract the fields from the trip_neg_details_6cases.txt file', 'extract_trip_neg_details')
    main(args)

