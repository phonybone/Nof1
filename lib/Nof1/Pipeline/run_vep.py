import os
from .run_cmd import RunCmd
from socket import gethostname

class RunVep(RunCmd):
    output_extension=".vep.out"

    def __init__(self, variants_fn, conf):
        self.variants_fn=variants_fn
        host=gethostname().split('.')[0]
        self.vep_script=conf.get(host, 'vep.script')
        self.cmd='perl'

    def get_cmd(self):
        return self.cmd

    def get_args(self):
        base=os.path.splitext(self.variants_fn)[0]
        output_fn=base+self.output_extension
        cmd=[self.vep_script, '-i', self.variants_fn, '--cache', '--format', 'guess', '-o', output_fn, '--force_overwrite']
        return cmd
    
    def get_environ(self):
        return {}
        
    
    
