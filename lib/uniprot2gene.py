from lazy import lazy

class uniprot2gene(object):
    def __init__(self, fn):
        self.fn=fn

    @lazy
    def u2g(self):
        ''' build dicts '''
        u2g,g2u=self._build_dicts()
        return u2g

    @lazy
    def g2u(self):
        u2g,g2u=self._build_dicts()
        return g2u

    def _build_dicts(self):
        self._u2g={}
        self._g2u={}
        with open(self.fn) as f:
            for r in f:
                try:
                    g,u=r.strip().split('\t')
                except ValueError:
                    continue
                
                try:
                    self._u2g[u].append(g)
                except KeyError:
                    self._u2g[u]=[g]

                try:
                    self._g2u[g].append(u)
                except KeyError:
                    self._g2u[g]=[u]
        return (self._u2g,self._g2u)

if __name__=='__main__':
    import os
    fn=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'g2u.tsv'))
    m=uniprot2gene(fn)

    for g,u in m.g2u.items():
        print 'g=%s, u=%s' % (g,u)

    expected=[
        ['SBF1', 'O95248'],     # g,u
        ['SCN7A', 'Q01118'],
        ['SEC24D', 'O94855'],
        ['SEC24D', 'A8K6V0'],
        ['SH3TC2', 'Q8TF17'],
        ['SLC13A3', 'Q8WWT9'],
        ['SLC13A3', 'A8MPP9'],
        ['SLC13A3', 'B4DF27'],
        ['SLC13A3', 'B4DIR8'],
        ['SPATA20', 'Q8TB22'],
        ['SSFA2', 'P28290'],
        ['STAM', 'Q92783'],
        ['STXBP5L', 'Q9Y2K9'],
        ['SULF1', 'Q8IWU6'],
        ['T', 'O15178'],
        ['TCEAL2', 'Q9H3H9'],
        ['TLK2', 'Q86UE8'],
        ['TMEM89', 'A2RUT3'],
        ['TOP2A', 'P11388'],
        ['TP53', 'P04637'],
        ['TP53', 'Q53GA5'],
        ['TRIM10', 'Q9UDY6'],
        ['TRIM10', 'Q5SRJ5']]
    for pair in expected:
        print 'pair is %s' % pair

        ge,ue=pair[0],pair[1]
        print 'ge=%s, ue=%s' % (ge,ue)
        g=m.u2g[ue]
        if ge not in g:
            print '%s: expected %s, got %s' % (ge, ue, m.u2g[ge])
        u=m.g2u[ge]
        if ue not in u:
            print '%s: expected %s, got %s' % (ue, ge, m.g2u[ue])
    print 'done'


            
