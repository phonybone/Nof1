from csv2rdfs import Csv2RDFs
from nof1_args import Nof1Args

def main(args):
    parser=Csv2RDFs()
    rdfs=parser.read()

    dao_rdf=dao_mongo(cls=RDF, db_name=na.args.db_name)
    n=0
    for rdf in rdfs:
        dao_rdf.save(rdf)
        n+=1
    print '%d rdfs saved' % n

if __name__ == '__main__':
    na=Nof1Args('nof1.conf')
    main(na.args)
