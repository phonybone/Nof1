import sys, os
libdir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','lib'))
sys.path.append(libdir)

from nof1_args import Nof1Args
from pyBabel.SmartClient import SmartClient

def main(args):
    print args
    id_types=['gene_ensembl','gene_symbol']
    babel=SmartClient().load(id_types)

    





if __name__=='__main__':
    config_fn=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'nof1.conf'))
    args=Nof1Args(config_fn, 'produce a report of all trip-neg genes, their targets, and drugs', 'gene_report')
    main(args.args)

