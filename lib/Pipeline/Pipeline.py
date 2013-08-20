from .exceptions import *

class Pipeline(object):
<<<<<<< HEAD
    def __init__(self, name, host, working_dir, dry_run):
        self.name=name
        self.host=host
        self.working_dir=working_dir
        self.dry_run=dry_run
=======
    def __init__(self, name, host, working_dir):
        self.name=name
        self.host=host
        self.working_dir=working_dir
>>>>>>> master

    def __repr__(self):
        return 'Pipeline %s: working_dir=%s' % (
            self.name, 
            self.working_dir)

    def run(self):
<<<<<<< HEAD
        raise AbstractMethodNotImplementedException('Pipeline.Pipeline.run')
=======
        raise AbstractMethodNotImplementedException('Nof1.Pipeline.Pipeline.run')
>>>>>>> master
