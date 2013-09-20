import sys, os

libdir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','lib'))
sys.path.append(libdir)
from nof1_args import Nof1Args


def main(args):
    if args.v: print args

    return 0


if __name__=='__main__':
    config_fn=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'nof1.conf'))
    args=Nof1Args(config_fn, '', 'nof1_report')
    sys.exit(main(args.args))
