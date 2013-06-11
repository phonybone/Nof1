import sys, os, re, csv
libdir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','lib'))
sys.path.append(libdir)

from nof1_args import Nof1Args
import django_env
import django
from data.models import Variation
from dump_obj import dump

def main(args):
    '''
    load the variation data from one of three sources (LOVD, umd, or nhgri) 
    into the database.
    '''
#    print args
    
    stats={'n_vars':0}
    fn=args.in_fn
    with open(fn) as f:
        reader=csv.reader(f, delimiter='\t')
        for line in reader:
            try:
                chrm=int(line[4])
                start=int(line[5])
                stop=int(line[6])
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
                    print '%d %d %d %s/%s %s' % (chrm, start, stop, ref, a1, strand)
#                    print '# %s %s' % (t1, t2)
                if a2 != ref:
                    print '%d %d %d %s/%s %s' % (chrm, start, stop, ref, a2, strand)
#                    print '# %s %s' % (t1, t2)
                
            except Exception, e:
                pass
#                print 'oops (%s): %s' % (type(e), e)


if __name__=='__main__':
    config_fn=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'nof1.conf'))
    args=Nof1Args(config_fn, 'extract the fields from the trip_neg_details_6cases.txt file', 'extract_trip_neg_details')
    main(args.args)

