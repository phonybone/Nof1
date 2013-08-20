import os
from .run_cmd import RunCmd

class RunFilterVep(RunCmd):
    output_extension="filtered"

    def __init__(self, host, working_dir, vep_out):
        super(RunFilterVep, self).__init__('filter_vep', host, working_dir)
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
        return ['%s.%s' % (os.path.splitext(self.vep_out)[0], self.output_extension)]
    
    
