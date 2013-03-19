from dao_mongo import dao_mongo

class DrugbankQueries(object):
    '''
    Encapsulation of common queries
    '''
    

    def gene2drugs(self, gene, dao):
        # gene->targets->drugs
        q1={'
