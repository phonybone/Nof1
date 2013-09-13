import re
from read1writeN import Read1WriteN

class RegexFileSplitter(object):
    '''
    split up a file into a number of other files based
    on regular expressions.  For each line in the input,
    apply a list of regexes; the first one matches determines which
    output file the line will get written to.
    '''
    def __init__(self, fn, *reg2fn):
        self.fn=fn
        self.reg2fn=reg2fn

    def __lol2dict(self, lol):
        d={}
        for pair in lol:
            d[pair[0]]=pair[1]
        return d

        
    def split(self):
        reg2fn=self.__lol2dict(self.reg2fn)
        with Read1WriteN(self.fn, **reg2fn) as r1wN:
            for line in r1wN.r1.readlines():
                for pair in self.reg2fn:
                    (reg,fn)=(pair[0],pair[1])
                    match=re.search(reg, line)
                    if match:
                        f=r1wN.k2f[match.group(0)]
                        f.write(line)
                        break

