import sys, os, csv
libdir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','lib'))
sys.path.append(libdir)

from nof1_args import Nof1Args
import django_env
import django
from data.models import Knowngene


def main(args):
    print args
    kg_set=read_kg(args)
    print 'kg: %d symbols' % len(kg_set)

    babel_set=read_babel(args)
    print 'babel: %d symbols' % len(babel_set)

    in_both=kg_set & babel_set
    print 'both: %d symbols' % len(in_both)

    kg_only=kg_set - babel_set
    print 'kg_only: %d symbols' % len(kg_only)

    babel_only=babel_set - kg_set
    print 'babel_only: %d symbols' % len(babel_only)


def read_kg(args):
    return _read_file(args.kg)

def read_babel(args):
    return _read_file(args.babel)

def _read_file(fn, delimiter='\t', field_no=0):
    s=set()
    with open(fn) as f:
        reader=csv.reader(f, delimiter=delimiter)
        for line in reader:
            s.add(line[field_no])
    return s

if __name__=='__main__':
    config_fn=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'nof1.conf'))
    args=Nof1Args(config_fn, 'find out how much babel and uscs knowngenes.txt overlap in terms of ucsc ids', 'kg_babel_overlap')
    main(args.args)

