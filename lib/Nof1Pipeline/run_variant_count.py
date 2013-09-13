from Pipeline.run_cmd import RunCmd

class RunVariantCount(RunCmd):
    output_extension='variants.count'
    def __init__(self, pipeline, 
                 data_basename, variant_basename,
                 skip_if_current=False):
        super(RunVariantCount, self).__init__('variant_count', pipeline, skip_if_current=skip_if_current)
        
        self.rnaseq_fn='%s.bt2.sam' % data_basename
        self.variant_fn=variant_basename
        self.out_fn='%s.%s' % (variant_basename, self.output_extension)

    def get_cmd(self):
        return self.pipeline.host.get('python.exe')

    def get_args(self):
        cmd=[self.pipeline.host.get('variant_count.script'), 
             '--variant_fn', self.variant_fn, 
             '--rnaseq_fn', self.rnaseq_fn,
             '--out_fn', self.out_fn]
        return cmd
    
    def get_environ(self):
        return {}
        
    def inputs(self):
        return [self.variant_fn, self.rnaseq_fn]

    def outputs(self):
        return [self.out_fn]
