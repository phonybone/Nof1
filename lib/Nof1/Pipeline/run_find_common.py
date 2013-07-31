import os
from .run_cmd import RunCmd
from socket import gethostname

class RunFindCommon(RunCmd):
    output_extension=".find_common.out"

    def __init__(self, fn1, fn2, conf):
        self.fn1=fn1
        self.fn2=fn2
        host=gethostname().split('.')[0]
        self.cmd=self.find_common_script=conf.get(host, 'find_common.script')
        

    def get_cmd(self):
        return self.cmd

    def get_args(self):
        cmd=[self.fn1, self.fn2]
        return cmd
    
    def get_environ(self):
        return {}
        
    
    
