import csv
from dao_mongo import dao_mongo
from rdf import RDF

class Csv2RDFs(object):
    def __init__(self, fn):
        self.fn=fn

    def read(self, **kwargs):
        rdfs=[]
        with open(self.fn) as f:
            reader=csv.reader(f, **kwargs)
            for row in reader:
                if len(row)==3:
                    rdfs.append(rdf(row[0], row[1], row[2]))
                elif len(row)==4:
                    rdfs.append(rdf(row[0], row[1], row[3]))
                elif len(row)==6:
                    rdf1=rdf(row[0], row[1], row[2]))
                    rdf2=rdf(row[3], row[4], row[5]))
                    
        return rdfs

