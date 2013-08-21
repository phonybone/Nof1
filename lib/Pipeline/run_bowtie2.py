import os
from .run_cmd import RunCmd

class RunBowtie2(RunCmd):
    def __init__(self, pipeline, data_basename, ref_index):
        super(RunBowtie2, self).__init__('bowtie2', pipeline)
        self.data_basename=data_basename
        self.ref_index=ref_index


    def get_cmd(self):
        return self.pipeline.host.get('bowtie2.exe')

    def get_args(self):
        index_path=os.path.join(self.pipeline.host.get('bowtie2.index_dir'), self.ref_index)
        input1='%s_1.fastq' % self.data_basename
        input2='%s_2.fastq' % self.data_basename
        output=self.outputs()[0]
        cmd=[index_path,
             '-p', self.pipeline.host.get('n_procs'),
             '-1', input1, 
             '-2', input2, 
             '-S', output]
        return cmd
    
    def get_environ(self):
        return {'BT2_INDEXES' : self.pipeline.host.get('bowtie2.index_dir')}

    def outputs(self):
        return ['%s.bt2.sam' % self.data_basename]
    
    
