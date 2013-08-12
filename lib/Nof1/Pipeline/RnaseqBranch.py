import sys
from Nof1.Pipeline import Pipeline
from Nof1.Pipeline.run_bowtie2 import RunBowtie2
from Nof1.Pipeline.run_rnaseq_count import RunRnaseqCount

class RnaseqBranch(Pipeline):
    '''
    this represents the Rnaseq branch of the Nof1 Pipeline.
    Not sure if we're still using it or not; definitely not finished as of 8/8/13.
    '''

    def __init__(self, 
                 host,          # host to run on
                 working_dir,   # directory to cd to; pathnames can be rel to this
                 data_basename, 
                 ref_index):
        super(RnaseqBranch, self).__init__('RnaseqBranch', host, working_dir)
        self.data_basename=data_basename
        self.ref_index=ref_index
        self.host=host
        self.working_dir=working_dir

    def run(self):
        RunBowtie2(self.host, self.working_dir, self.data_basename, self.ref_index).run()
        RunRnaseqCount(self.host, self.working_dir, self.data_basename).run()

