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
    
    g_syn=args.gene
    dt_dao=dao_mongo(cls=rdf.graph, db=args.db_name)

    query={'pred':'Synonyms', 'obj':g_syn}
    drugs=dt_dao.find(query, collection=args.collection)
#    print '%s: %d results' % (query, len(drugs))
    for d in drugs:
        print d

        query={'pred':'Drug(s)', 'sub':d.sub}
#        print query
        targets=dt_dao.find(query, collection=args.collection)
        print '%d targets for %s' % (len(targets), d.sub)
        for t in targets:
            print t
        print

#        print dump(t)
#        print '%s: %s: gene=%s' % (str(t.ID[0]), str(t.Name[0]), str(t.Gene_Name[0]))




if __name__=='__main__':
    from nof1_args import Nof1Args
    conf_fn=os.path.join(rootdir, 'nof1.conf')
    args=Nof1Args(conf_fn, 'script to compile stats about Nof1 dbs', 'gene2targets')
    main(args.args)
