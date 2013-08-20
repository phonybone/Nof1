from .exceptions import *

class Pipeline(object):
    def __init__(self, name, host, working_dir):
        self.name=name
        self.host=host
        self.working_dir=working_dir

    def __repr__(self):
        return 'Pipeline %s: working_dir=%s' % (
            self.name, 
            self.working_dir)

    def run(self):
        raise AbstractMethodNotImplementedException('Nof1.Pipeline.Pipeline.run')
