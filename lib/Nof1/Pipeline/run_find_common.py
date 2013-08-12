import os
from .run_cmd import RunCmd
from socket import gethostname

class RunFindCommon(RunCmd):
    output_extension=".find_common.out"

    def __init__(self, host, working_dir, f1, f2):
        super(RunRnaseq, self).__init__('find_common', host, working_dir)
        self.data_basename=data_basename

        self.fn1=fn1
        self.fn2=fn2
        

    def get_cmd(self):
        return self.

    def get_args(self):
        cmd=[self.fn1, self.fn2]
        return cmd
    
    def get_environ(self):
        return {}
        
    
    
