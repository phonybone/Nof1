import os
from Pipeline.run_cmd import RunCmd

class RunReport(RunCmd):
    def __init__(self, pipeline, 
                 combined_genes_fn, out_fn=None,
                 skip_if_current=False):
        super(RunReport, self).__init__('report', pipeline, skip_if_current=skip_if_current)
        self.combined_genes_fn=combined_genes_fn
        self.out_fn=out_fn

    def get_cmd(self):
        return self.pipeline.host.get('python.exe')

    def get_args(self):
        cmd=[self.pipeline.host.get('report.script'), 
             self.combined_genes_fn]
        if self.out_fn: 
            cmd.extend(['--out_fn', self.out_fn])
        return cmd
    
    def get_environ(self):
        return {}

    def inputs(self):
        return [self.combined_genes_fn]

    def outputs(self):
        return [self.out_fn] if self.out_fn else []
    
    
