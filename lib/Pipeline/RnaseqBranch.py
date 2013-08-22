from Pipeline import Pipeline
from .run_bowtie2 import RunBowtie2
from .run_rnaseq_count import RunRnaseqCount
from .exceptions import *

class RnaseqBranch(Pipeline):
    '''
    this represents the Rnaseq branch of the Nof1 Pipeline.
    Not sure if we're still using it or not; definitely not finished as of 8/8/13.
    '''

    def __init__(self, 
                 host,          # host to run on
                 working_dir,   # directory to cd to; pathnames can be rel to this
                 data_basename, 
                 ref_index,
                 dry_run=False,
                 output_dir=None):
        super(RnaseqBranch, self).__init__('RnaseqBranch', host, working_dir, output_dir, 
                                           dry_run=dry_run)
        self.data_basename=data_basename
        self.ref_index=ref_index
        self.host=host
        self.working_dir=working_dir

        self.bt2=RunBowtie2(self, data_basename, ref_index)
        self.rc=RunRnaseqCount(self, data_basename)
        

    def run(self):
        self._run_cmds(self.bt2, self.rc)

    def outputs(self):
        return self.rc.outputs()
