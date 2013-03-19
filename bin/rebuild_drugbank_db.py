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
    dao_dc=dao_mongo(cls=Drugcard, db=args.db_name)
    dao_dc.remove()

    builder=DrugcardBuilderFactory().get_instance(args.builder)
    reader=DrugbankReader(fn=args.in_fn, builder=builder)
    stats={'n_saved':0}
    for dc in reader:
        dao_dc.save(dc)
        print '%s saved' % dc.id
        stats['n_saved']+=1
    print dump(stats)




if __name__=='__main__':
    config_fn=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'nof1.conf'))
    args=Nof1Args(config_fn, 'rebuild drugbank database', 'rebuild_db')
    main(args.args)
