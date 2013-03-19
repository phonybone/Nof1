import os, sys
from itertools import izip_longest

rootdir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
sys.path.append(os.path.join(rootdir, 'lib'))
from dao_mongo import dao_mongo
from drugcard import Drugcard
from drugtarget import DrugTarget
from dump_obj import dump
import rdf

def main(args):
    print args
    
    path=args.path
    dt_dao=dao_mongo(cls=rdf.graph, db=args.db_name)

    query={'pred':'Pathway', 'obj':path}
    drugs=dt_dao.find(query, collection=args.collection)
    for d in drugs:

        query={'pred':'Drug(s)', 'sub':d.sub}
        targets=dt_dao.find(query, collection=args.collection)
        if len(targets)==0: continue
        print d

        s='' if len(targets)==1 else 's'
        print '%d target%s for %s' % (len(targets), s, d.sub)
        for t in targets:
            print t
        print



if __name__=='__main__':
    from nof1_args import Nof1Args
    conf_fn=os.path.join(rootdir, 'nof1.conf')
    args=Nof1Args(conf_fn, 'script to compile stats about Nof1 dbs', 'path2targets')
    main(args.args)
