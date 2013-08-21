from .run_cmd import RunCmd

class RunRnaseqCount(RunCmd):
    output_extension='genes.count'
    def __init__(self, pipeline, data_basename):
        super(RunRnaseqCount, self).__init__('rnaseq_count', pipeline)
        self.data_basename=data_basename
        self.in_fn='%s.bt2.sam' % self.data_basename
        self.out_fn='%s.%s' % (self.data_basename, self.output_extension)

    def get_cmd(self):
        return self.pipeline.host.get('python.exe')

    def get_args(self):
        cmd=[self.pipeline.host.get('rnaseq_count.script'), 
             '--in_fn', self.in_fn, 
             '--out_fn', self.out_fn]
        return cmd
    
    def get_environ(self):
        return {}
        
    
    def outputs(self):
        return [self.out_fn]
