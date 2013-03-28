import sys, os
libdir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','lib'))
sys.path.append(libdir)

from nof1_args import Nof1Args
from drugbank_reader import DrugbankReader
from drugcard import Drugcard
from drugcard_builder_factory import DrugcardBuilderFactory
from dao_mongo import dao_mongo
from dump_obj import dump

def main(args):
    print args

    builder=DrugcardBuilderFactory().get_instance(args.builder, 
                                                  clear_table=args.clear_table,
                                                  uniprot_gene_fn=args.uniprot_gene_fn)
    reader=DrugbankReader(fn=args.in_fn, builder=builder)
    for dc in reader:
        print '%s saved' % dc.id
    print dump(builder.stats)




if __name__=='__main__':
    config_fn=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'nof1.conf'))
    args=Nof1Args(config_fn, 'rebuild drugbank database', 'rebuild_db')
    main(args.args)
