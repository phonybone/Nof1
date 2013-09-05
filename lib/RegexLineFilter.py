class RegexLineFilter(object):
    '''
    Class to filter a text file, line by line, based on ordered regexs.
    Takes a list of regex/filename pairs; for each line, the first regex
    that matches the line sends the output to the corresponding file.
    '''

    def __init__(self, in_fn, regex2out_fn):
        
