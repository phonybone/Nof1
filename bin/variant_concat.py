import sys, os, glob

libdir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','lib'))
sys.path.append(libdir)
from nof1_args import Nof1Args

'''
Stupid script needed because I can't figure out how to make python.subprocess
handle redirection symbols correctly.  grrr.
'''

def main(args):
    if args.v: print args
    with open(args.out_fn, 'w') as output:
        for file in glob.glob('%s/*.fastq' % args.variant_dir):
            if args.v: print file
            with open(file) as f:
                output.write(f.read())

    if args.v: print '%s written' % args.out_fn
    return 0


if __name__=='__main__':
    config_fn=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'nof1.conf'))
    args=Nof1Args(config_fn, 'concat variant.sam files', 'variant_concat')
    sys.exit(main(args.args))
