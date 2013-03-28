
class TtdBuilderSqlite(object):
    def __init__(self):
        pass

    def on_line3(self, row):
        print 'line3 called'
    
    def on_line4(self, row):
        print 'line4 called'
    
    def on_line6(self, row):
        print 'line6 called'
        
    def on_end(self):
        raise Exception('nyi')

    
    
