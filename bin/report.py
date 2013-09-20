import sys, os

libdir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','lib'))
sys.path.append(libdir)
from nof1_args import Nof1Args
from reporter import Reporter
from Pipeline.host import Host

def main(args):
    if args.v: print args

    genes=read_genes(args)
    if args.v: print '%d genes' % len(genes)

    reporter=Reporter(Host(), genes)

    try:
        out=open(args.out_fn, 'w')
    except IOError:
        out=sys.stdout
    except TypeError:
        out=sys.stdout

    out.write(reporter.report())
    for k in sorted(reporter.stats.keys()):
        out.write('%-20s: %s\n' % (k,reporter.stats[k]))

    if out != sys.stdout:
        out.close()

    return 0


def read_genes(args):
    genes=set()
    with open(args.genes_fn) as f:
        for line in f.readlines():
            genes.add(line.strip())
#        genes=f.read().splitlines()
    return genes

if __name__=='__main__':
    config_fn=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'nof1.conf'))
    args=Nof1Args(config_fn, 'Nof1 report', 'report')
    sys.exit(main(args.args))
