from Pipeline.Pipeline import Pipeline
from .run_bowtie2 import RunBowtie2
from .run_rnaseq_count import RunRnaseqCount
from .run_variant_count import RunVariantCount
from .run_variant_splitter import RunVariantSplitter
from .run_variant_concat import RunVariantConcat
from Pipeline.exceptions import *

class RnaseqBranch(Pipeline):
    '''
    this represents the Rnaseq branch of the Nof1 Pipeline.
    '''

    def __init__(self, 
                 host,          # host to run on
                 working_dir,   # directory to cd to; pathnames can be rel to this
                 data_basename, 
                 ref_index,
                 variant_fn,
                 variants_dir,
                 dry_run=False,
                 output_dir=None,
                 echo=False,
                 skip_if_current=False):
        super(RnaseqBranch, self).__init__('RnaseqBranch', host, working_dir, 
                                           output_dir=output_dir, dry_run=dry_run, echo=echo,
                                           skip_if_current=skip_if_current)
        self.data_basename=data_basename
        self.ref_index=ref_index

        self.add_cmd(RunBowtie2(self, data_basename, ref_index, skip_if_current))
#        self.add_cmd(RunRnaseqCount(self, data_basename, skip_if_current))

        self.add_cmd(RunVariantSplitter(self, data_basename, variant_fn, variants_dir, skip_if_current))
        self.add_cmd(RunVariantConcat(self, variants_dir, variant_fn, skip_if_current))
        self.add_cmd(RunVariantCount(self, self.variant_concat.outputs()[0], variant_fn, skip_if_current))

    def run(self):
        self._run_cmds()

    def outputs(self):
#        return self.rnaseq_count.outputs()
        return self.variant_count.outputs()
