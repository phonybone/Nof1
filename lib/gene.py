def readgenes(fn):
    ''' load the same genes that Ram gave us '''
    with open(fn) as f:
        samgenes=[x.strip() for x in f]
    return samgenes

