import csv
from dao_mongo import dao_mongo
import rdf

class ttd_reader(object):
    def __init__(self, fn, n_burn=10, fuse=-1):
        self.fn=fn
        self.n_burn=n_burn
        self.fuse=fuse

    def read(self, **kwargs):   # kwargs get passed to csv.reader
        '''
        Read the TTD_download.txt file.  Burn the first <n_burn> lines of header.
        Each line has either 3,4, or 6 values:
        If 3: return the rdf triple
        If 4: f3 is the name for f4, so return (f1,f2,f4) and (f4, 'name', f3)
        If 6: compound statement: f3 'targets' f1 'for disease' f5 'in testing phase' f6


f2 is always 'Drug(s)', but it also implies a 'for disease' clause.
              so alter f2 accordingly.  
f3 names f4, so (f4 'name' f3)
              
        '''
        g=rdf.graph()
        with open(self.fn) as f:
            if self.n_burn > 0:
                print 'n_burn: %s' % self.n_burn
                for i in xrange(self.n_burn):
                    f.readline()

            fuse=self.fuse
            reader=csv.reader(f, delimiter='\t')
            for row in reader:

                # cleanup for utf-8:
                r2=[]
                for r in row:
                    r2.append(self.utf_clean(r))
                row=r2

                if len(row)==3:
                    g.add_triple(rdf.triple(sub=row[0], pred=row[1], obj=row[2]))
                elif len(row)==4:
                    g.add_triple(rdf.triple(sub=row[0], pred=row[1], obj=row[3]))
                    g.add_triple(rdf.triple(sub=row[3], pred='name', obj=row[2]))
                elif len(row)==6:
                    drug=rdf.triple(sub=row[3], pred=row[4], obj=row[5])
                    target=rdf.triple(sub=row[0], pred=row[1], obj=drug)
                    g.add_triple(target)

                if fuse==0: break
                fuse -= 1
                    
        return g

    def utf_clean(self, s):
        try:
            return s.decode('utf-8')
        except UnicodeDecodeError:
            new_s=[]
            for c in s:
                try:
                    new_s.append(c.decode('utf-8'))
                except UnicodeDecodeError:
                    new_s.append('?')
            return ''.join(new_s)
