class read1write2(object):
    '''
    Object to be used within a with statement; opens one file for reading and two for writing
    Needs more testing, 
    '''
    def __init__(self, rn1, wn1, wn2):
        self.rn1=rn1
        self.wn1=wn1
        self.wn2=wn2

    def __enter__(self):
        self.r1=open(self.rn1, 'r')
        self.w1=open(self.wn1, 'w')
        self.w2=open(self.wn2, 'w')
        return self

    def __exit__(self, type, value, tb):
        self.r1.close()
        self.w1.close()
        self.w2.close()
