import os
from Pipeline.run_cmd import RunCmd
from run_rnaseq_count import RunRnaseqCount
from run_muts2vep import RunMuts2Vep

class RunCombine(RunCmd):
    out_extension='.combined'
    def __init__(self, pipeline,
                 gene_counts_fn, auto_fn, polyphen_sift_fn,
                 out_fn=None,
                 skip_if_current=False,
                 ):
        super(RunCombine, self).__init__('combine_rnaseq_vep', pipeline, 
                                         skip_if_current=skip_if_current)
        self.gene_counts_fn=gene_counts_fn
        self.auto_fn=auto_fn
        self.polyphen_sift_fn=polyphen_sift_fn

        if out_fn:
            self.out_fn=out_fn
        else:
            self.out_fn=os.path.join(pipeline.working_dir,
                                     '%s.%s%s' % (os.path.basename(gene_counts_fn), 
                                                  os.path.basename(auto_fn),
                                                  self.out_extension))

    def get_cmd(self):
        return self.pipeline.host.get('python.exe')

    def get_args(self):
        cmd=[self.pipeline.host.get('combine.script'), 
             self.gene_counts_fn,
             self.auto_fn,
             self.polyphen_sift_fn,
             '--out_fn', self.out_fn,
             '-v',
             ]
        return cmd
    
    def get_environ(self):
        return {}

    def inputs(self):
        return [self.gene_counts_fn, self.auto_fn, self.polyphen_sift_fn]

    def outputs(self):
        return [self.out_fn]
    
    
