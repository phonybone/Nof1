from Pipeline.run_cmd import RunCmd

class RunVariantSplitter(RunCmd):
    output_extension='variants.count'
    def __init__(self, pipeline, 
                 data_basename, variant_basename, output_dir,
                 skip_if_current=False):
        super(RunVariantSplitter, self).__init__('variant_splitter', pipeline, skip_if_current=skip_if_current)
        
        self.rnaseq_fn='%s.sam' % data_basename
        self.variant_fn=variant_basename
        self.output_dir=output_dir

    def get_cmd(self):
        return self.pipeline.host.get('python.exe')

    def get_args(self):
        cmd=[self.pipeline.host.get('variant_splitter.script'), 
             '--variant_fn', self.variant_fn, 
             '--rnaseq_fn', self.rnaseq_fn,
             '--output_dir', self.output_dir]
        return cmd
    
    def get_environ(self):
        return {}
        
    def inputs(self):
        return [self.variant_fn, self.rnaseq_fn]

    def outputs(self):
        return [self.output_dir]
