import os
from .run_cmd import RunCmd

class RunVep(RunCmd):
    output_extension=".vep.filtered"

    def __init__(self, host, working_dir, vep_out):
        super(RunVep, self).__init__('vep', host, working_dir)
        self.vep_out=vep_out

    def get_cmd(self):
        return 'python'

    def get_args(self):
        output_fn=self.outputs()[0]
        cmd=[self.host.get('filter_vep.script'),
             self.vep_out,
             ]
        return cmd
    
    def get_environ(self):
        return {}
        
    def outputs(self):
        return [os.path.splitext(self.vep_out)[0] + self.output_extension] # also a .html file!
    
    
