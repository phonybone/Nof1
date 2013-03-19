import sys, os
libdir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','lib'))
sys.path.append(libdir)

from nof1_args import Nof1Args
from ttd_reader import ttd_reader
from dao_mongo import dao_mongo
import rdf
from dump_obj import dump

def main(args):
    print args

    gd=dao_mongo(cls=rdf.graph, db=args.db_name, collection='ttd')
    gd.remove()
    gd.ensure_index('sub')
    gd.ensure_index('pred')
    gd.ensure_index('obj')
#    gd.ensure_index([('sub',1),('pred',1),('obj',1)], unique=True) # skrews up when all are None
    gd.ensure_index([('sub',1),('pred',1),('obj',1)])

    reader=ttd_reader(args.in_fn, args.burn_lines)
    g=reader.read()
    print '%d items in graph' % len(g)
    
    stats={'n':0}
    for t in g.triples:
        id=gd.save(t)
        stats['n']+=1

    print dump(stats)

if __name__=='__main__':
    config_fn=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'nof1.conf'))
    args=Nof1Args(config_fn, 'rebuild drugbank database', 'rebuild_ttd')
    main(args.args)
