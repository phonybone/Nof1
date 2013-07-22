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
                    istart=int(start)
                except:
                    sys.stderr.write("can't convert %s to int\n" % start)
                    continue
                stop=line[6]
                strand=line[7]
                t1=line[8]
                t2=line[9]
                ref=line[10]
                a1=line[11]
                a2=line[12]
                '''
                print 'chrm: %s' % chrm
                print 'start: %s' % start
                print 'stop: %s' % stop
                print 'strand: %s' % strand
                print 'ref: %s' % ref
                print 'a1: %s' % a1
                print 'a2: %s' % a2
                print
                '''
                if a1 != ref:
                    print '%s %s %s %s/%s %s %s' % (chrm, start, stop, ref, a1, strand, sym)
#                    print '# %s %s' % (t1, t2)
                if a2 != ref:
                    print '%s %s %s %s/%s %s %s' % (chrm, start, stop, ref, a2, strand, sym)
#                    print '# %s %s' % (t1, t2)
                
            except Exception, e:
                print 'caught %s' % e
                traceback.print_exc()
#                traceback.print_exception(sys.exc_type, sys.exc_value, sys.exc_traceback, None, sys.stderr)
                pass
#                print 'oops (%s): %s' % (type(e), e)


if __name__=='__main__':
    config_fn=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'nof1.conf'))
    args=Nof1Args(config_fn, 'extract the fields from the trip_neg_details_6cases.txt file', 'extract_trip_neg_details')
    main(args)

