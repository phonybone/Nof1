import os, sys
from itertools import izip_longest

rootdir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..'))
sys.path.append(os.path.join(rootdir, 'lib'))
from dao_mongo import dao_mongo
from drugcard import Drugcard
from drugtarget import DrugTarget
from dump_obj import dump

def main(args):
    print args
    
    
    dt_dao=dao_mongo(cls=Drugcard, db=args.db_name)

    query={}
    for k,v in grouper(2, args.query):
        query[k]=v
    print 'query: %s' % query


    targets=dt_dao.find(query, collection=args.collection)
    print '%s: %d results' % (query, len(targets))
    for t in targets:
        print t
#        print dump(t)
#        print '%s: %s: gene=%s' % (str(t.ID[0]), str(t.Name[0]), str(t.Gene_Name[0]))




def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return izip_longest(fillvalue=fillvalue, *args)

if __name__=='__main__':
    from nof1_args import Nof1Args
    conf_fn=os.path.join(rootdir, 'nof1.conf')
    args=Nof1Args(conf_fn, 'script to compile stats about Nof1 dbs', 'query')
    main(args.args)
