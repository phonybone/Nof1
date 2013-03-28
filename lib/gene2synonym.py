from lazy import lazy

class gene2synonyms(object):
    def __init__(self, fn):
        self.fn=fn

    # should make this a singleton class, one way or another
    # doesn't even really need to be a class

    @lazy
    def g2s(self):
        ''' build dicts '''
        g2s,s2g=self._build_dicts()
        return g2s

    @lazy
    def s2g(self):
        g2s,s2g=self._build_dicts()
        return s2g

    def _build_dicts(self):
        self._g2s={}
        self._s2g={}
        with open(self.fn) as f:
            for r in f:
                try:
                    g,s=r.strip().split('\t')
                except ValueError:
                    continue

                try:
                    self._g2s[g].append(s)
                except KeyError:
                    self._g2s[g]=[s]

                try:
                    self._s2g[s].append(g)
                except KeyError:
                    self._s2g[s]=[g]
        return (self._g2s,self._s2g)

if __name__=='__main__':
    import os, sys
    from dump_obj import dump

    fn=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'gene2synonym.tsv'))
#    fn=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'g2s.7.tsv'))
    m=gene2synonyms(fn)
    g2s=m.g2s


    expected=[
        ['Org5', 'ORG7.1'],
        ['Bwtn4', 'WTN12.1'],
        ['Lbn10', 'LBN17.1'],
        ['Mofp5', 'Mof5'],
        ['Rfpw5', 'Rf5'],
        ['Bmd28', 'Bmd21'],
        ['Bmd33', 'Bmd26'],
        ['Pbft3', 'Pbf3'],
        ['Kwq15', 'Kwq9'],
        ['Sox10m3', 'Agln2'],
        ['Sox10m3', 'Agln3'],
        ['Blacv1', 'Vol8a'],
        ['Hbnr2', 'Hpnr2'],
        ['T2dm1sa', 'Nfbg'],
        ['Hipp5', 'DGVi11a'],
        ['Sdtq2', 'L2'],
        ['Impbw1', 'Bmq3'],
        ['Scgq1', 'Scg-1'],
        ['Org1', 'ORG2.1'],
        ['CDH1', 'Arc-1'],
        ['CDH1', 'CD324'],
        ['CDH1', 'CDHE'],
        ['CDH1', 'LCAM'],
        ['NAT1', 'AAC1'],
        ['NAT1', 'MNAT'],
        ['NAT1', 'NATI'],
        ]

    stats={'n_found':0, 'n_missing':0}
    for pair in expected:
        ge,se=pair[0],pair[1]
        try:
            g=m.s2g[se]
            if ge not in g:
                print '%s: expected %s, got %s' % (se, ge, m.s2g[se])
                stats['n_missing']+=1
            else:
                stats['n_found']+=1
        except KeyError:
            print 'nothing found for %s: Expected %s' % (ge, se)

        try:
            s=m.g2s[ge]
            if se not in s:
                print '%s: expected %s, got %s' % (se, ge, m.g2s[ge])
                stats['n_missing']+=1
            else:
                stats['n_found']+=1
        except KeyError:
            print 'nothing found for %s: Expected %s' % (se, ge)

    print '%s: %s' % ('CDH1', m.g2s['CDH1'])
    print '%s: %s' % ('LCAM', m.s2g['LCAM'])

    print 'done: %s' % stats


            
