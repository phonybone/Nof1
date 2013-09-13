import sys, os

libdir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','lib'))
sys.path.append(libdir)
from nof1_args import Nof1Args
from variant_counter import VariantCounter

def main(args):
    if args.v: print args
    try:
        return VariantCounter(args).go()
    except Exception, e:
        import traceback
        traceback.print_exc()
        
        return 1



if __name__=='__main__':
    config_fn=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'nof1.conf'))
    args=Nof1Args(config_fn, 'attempt to calculate some measure of variant expression using a variants file and an rnaseq input', 'variant_count')
    sys.exit(main(args.args))
