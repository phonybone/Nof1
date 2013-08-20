import sys, os

libdir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','lib'))
sys.path.append(libdir)
from nof1_args import Nof1Args
from VepPolyphenSIFTFilter import VepPolyphenSIFTFilter


def main(args):
    if args.v: print args

    filter=VepPolyphenSIFTFilter(args.in_fn)
    stats=filter.go()
    if args.v: 
        print '%s written' % filter.vep_filtered_fn
        for k in sorted(stats.keys()):
            print '%s: %d' % (k, stats[k])

if __name__=='__main__':
    config_fn=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'nof1.conf'))
    args=Nof1Args(config_fn, 'filter vep output based on polyphen and SIFT predictions', 'filter_vep')
    main(args.args)
