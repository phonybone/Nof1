from .exceptions import *

class Pipeline(object):
    def __init__(self, name, host, working_dir, dry_run=False):
        self.name=name
        self.host=host
        self.working_dir=working_dir
        self.dry_run=dry_run

    def __repr__(self):
        return 'Pipeline %s: working_dir=%s' % (
            self.name, 
            self.working_dir)

    def run(self):
        raise AbstractMethodNotImplementedException('Pipeline.Pipeline.run')
