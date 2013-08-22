import os, tempfile, logging
from Pipeline import Pipeline
from .VEPBranch import VEPBranch
from .RnaseqBranch import RnaseqBranch
from .run_combine import RunCombine
from .exceptions import *

class Nof1Pipeline(Pipeline):
    log=logging.getLogger(__name__)
    def __init__(self, host, working_dir, data_basename, ref_index, variants_fn, 
                 dry_run=False, output_dir=None):
        super(Nof1Pipeline, self).__init__('Main', host, working_dir, output_dir, dry_run=dry_run)
        self.data_basename=data_basename
        self.ref_index=ref_index
        self.variants_fn=variants_fn
        
        self.rnaseq_branch=RnaseqBranch(host, working_dir, data_basename, ref_index, 
                                        dry_run=dry_run, output_dir=output_dir)

        self.vep_branch=VEPBranch(host, working_dir, variants_fn,
                                  dry_run=dry_run, output_dir=output_dir)
        
        self.combine=RunCombine(self,
                                self.rnaseq_branch.outputs()[0], # .genes.count
                                self.vep_branch.outputs()[0],    # .auto
                                self.vep_branch.outputs()[1],    # .vep.filtered
                                )

    def run(self):
        os.chdir(self.working_dir)
        self._create_output_dir()

        try:
            self.rnaseq_branch.run()
            self.vep_branch.run()
            self.combine.run()
        except PipelineException, e:
            print e


        
