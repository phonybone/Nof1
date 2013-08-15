class Read1WriteN(object):
    '''
    Object to be used within a with statement; opens one file for reading and N for writing
    Needs more testing, 
 
    Need to rewrite this: change *wN to **wN, and use the keys as the attr names and 
    the values as the filenames.

    Then rewrite the test to reflect that (or rewrite the test first!)

    '''
    def __init__(self, rn1, **k2fn):
        self.rn1=rn1
        self.k2fn=k2fn
        self.k2f={}

    def __str__(self):
        s='rn1: %s\n' % self.rn1
        for key in sorted(self.k2fn.keys()):
            s+='%s -> %s\n' % (key, self.k2fn[key])
        return s

    def __enter__(self):
        self.r1=open(self.rn1, 'r')
        for key, fn in self.k2fn.items():
            f=open(fn, 'w')
            self.k2f[key]=f
        return self

    def __exit__(self, type, value, tb):
        self.r1.close()
        for f in self.k2f.values():
            f.close()


