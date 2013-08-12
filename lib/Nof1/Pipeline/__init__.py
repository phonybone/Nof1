from exceptions import *

class Pipeline(object):
    def __init__(self, name, host, output_dir):
        self.name=name
        self.output_dir=output_dir

    def __repr__(self):
        return 'Pipeline %s: output_dir=%s' % (
            self.name, 
            self.output_dir)

    def run(self):
        raise AbstractMethodNotImplementedException('Nof1.Pipeline.Pipeline.run')
