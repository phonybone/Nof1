import os
from .run_cmd import RunCmd

class RunFilterVep(RunCmd):
    output_extension="filtered"

    def __init__(self, pipeline, vep_out, skip_if_current=False):
        super(RunFilterVep, self).__init__('filter_vep', pipeline, skip_if_current=skip_if_current)
        self.vep_out=vep_out

    def get_cmd(self):
        return self.pipeline.host.get('python.exe')

    def get_args(self):
        output_fn=self.outputs()[0] # used???
        cmd=[self.pipeline.host.get('filter_vep.script'),
             '--in_fn', self.inputs()[0],
             '-v'
             ]
        return cmd
    
    def get_environ(self):
        return {}
        
    def inputs(self):
        return [self.vep_out]

    def outputs(self):
#        return ['%s.%s' % (os.path.splitext(self.vep_out)[0], self.output_extension)]
        return ['%s.%s' % (                  self.vep_out    , self.output_extension)]
    
    
