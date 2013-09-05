import sys, os

libdir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','lib'))
sys.path.append(libdir)
from nof1_args import Nof1Args
from variant_counter import VariantCounter

def main(args):
    if args.v: print args
    sys.exit(VariantCounter(args).go())



if __name__=='__main__':
    config_fn=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'nof1.conf'))
    args=Nof1Args(config_fn, 'attempt to calculate some measure of variant expression using a variants file and an rnaseq input', 'variant_count')
    main(args.args)
