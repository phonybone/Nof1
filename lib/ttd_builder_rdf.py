import rdf

class TtdBuilderRdf(object, **kwargs):
    def __init__(self):
        self.g=rdf.graph
#        self.dao=kwargs['dao']
        self.dao=dao_mongo(cls=rdf.graph, db=kwargs['db_name'])

    def on_line3(self, row):
        self.g.add_triple(rdf.triple(sub=row[0], pred=row[1], obj=row[2]))
    
    def on_line4(self, row):
        self.g.add_triple(rdf.triple(sub=row[0], pred=row[1], obj=row[3]))
        self.g.add_triple(rdf.triple(sub=row[3], pred='name', obj=row[2]))        
    
    def on_line6(self, row):
        drug=rdf.triple(sub=row[3], pred=row[4], obj=row[5])
        target=rdf.triple(sub=row[0], pred=row[1], obj=drug)
        g.add_triple(target)
        
    def on_eof(self):
        for t in self.g.triples:
            id=self.dao.save(t)

        return self.g
    
    
