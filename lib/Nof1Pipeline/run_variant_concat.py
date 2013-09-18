from Pipeline.run_cmd import RunCmd

class RunVariantConcat(RunCmd):
    output_extension='variants.sam'
    def __init__(self, pipeline, 
                 variant_dir, variant_basename,
                 skip_if_current=False):
        super(RunVariantConcat, self).__init__('variant_concat', pipeline, 
                                               skip_if_current=skip_if_current,
                                               is_shell=False)
        
        self.variant_out_fn='%s.%s' % (variant_basename, self.output_extension)
        self.variant_dir=variant_dir

    def get_cmd(self):
        return self.pipeline.host.get('python.exe')

    def get_args(self):
        cmd=[self.pipeline.host.get('variant_concat.script'),
             '--variant_dir', self.variant_dir,
             '--out_fn', self.variant_out_fn,
         ]
        return cmd
    
    def get_environ(self):
        return {}
        
    def inputs(self):
        return [self.variant_dir]

    def outputs(self):
        return [self.variant_out_fn]
