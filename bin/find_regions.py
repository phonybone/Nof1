'''
Program to merge Ram's dbSNP_Cancer_pipeline_regions.txt file
'''

import sys, os, csv

libdir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','lib'))
sys.path.append(libdir)
from nof1_args import Nof1Args
from chr_range import *


def main(args):
    if args.v: print args
    stats={'n_fragments':0,
           'n_regions':0}

    with open(args.in_fn) as f:
        reader=csv.reader(f, delimiter=args.delimiter)
        
        row=reader.next()
        current=ChrRange(*row)
        print 'row is %s' % row
        print 'current is %s' % current

        for row in reader:
            (chr, start, stop)=row
            try:
                cr=ChrRange(chr, int(start), int(stop))
                stats['n_fragments']+=1
                if cr.chr not in stats:
                    stats[cr.chr]={}
                try: stats[cr.chr]['n_fragments']+=1
                except KeyError: stats[cr.chr]['n_fragments']=1
                    
                    
            except ChrException, e:
                print 'caught %s' % e
                continue

            if cr.chr == current.chr and cr.start < current.start:
                raise Exception('unsorted regions: cr=%s, current=%s' % (cr, current))

            if cr.overlaps(current):
                current.stop=max(current.stop, cr.stop)
            else:
                print current
                current=cr
                stats['n_regions']+=1
                try: stats[cr.chr]['n_regions']+=1
                except KeyError: stats[cr.chr]['n_regions']=1

    for k in sorted(stats.keys()):
        d=stats[k]
        try:
            print '%s: n_fragments: %d' % (k, d['n_fragments'])
            print '%s: n_regions: %d' % (k, d['n_regions'])
        except TypeError:
            pass
    print 'total fragments: %d' % stats['n_fragments']
    print 'total regions: %d' % stats['n_regions']



if __name__=='__main__':
    config_fn=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'nof1.conf'))
    args=Nof1Args(config_fn, 'Find continuous regions by grouping together smaller ones (data-specific program)', os.path.splitext(os.path.basename(__file__))[0])
    main(args.args)
