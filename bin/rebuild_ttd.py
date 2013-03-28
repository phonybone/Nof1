import sys, os
libdir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','lib'))
sys.path.append(libdir)

from nof1_args import Nof1Args
from ttd_reader import ttd_reader
from ttd_builder_factory import TtdBuilderFactory
from dao_factory import dao_factory
import rdf
from dump_obj import dump

def main(args):
    print args

    builder=TtdBuilderFactory().get_instance(args.builder, db=args.db_name, 
                                             clear_table=args.clear_table,
                                             uniprot_gene_fn=args.uniprot_gene_fn)
    reader=ttd_reader(args.in_fn, builder, args.burn_lines)
    g=reader.read()
    print dump(builder.stats)

if __name__=='__main__':
    config_fn=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'nof1.conf'))
    args=Nof1Args(config_fn, 'rebuild drugbank database', 'rebuild_ttd')
    main(args.args)
