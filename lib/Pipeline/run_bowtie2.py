import os
from .run_cmd import RunCmd

class RunBowtie2(RunCmd):
    def __init__(self, pipeline, data_basename, ref_index, skip_if_current=False):
        super(RunBowtie2, self).__init__('bowtie2', pipeline, skip_if_current=skip_if_current)
        self.data_basename=data_basename
        self.ref_index=ref_index


    def get_cmd(self):
        return self.pipeline.host.get('bowtie2.exe')

    def get_args(self):
        index_path=os.path.join(self.pipeline.host.get('bowtie2.index_dir'), self.ref_index)
        inputs=self.inputs()
        output=self.outputs()[0]
        cmd1=[index_path,
             '-p', self.pipeline.host.get('n_procs'),
             '-1', inputs[0],
             '-2', inputs[1],
             '-S', output]
        return cmd1
    
    def get_environ(self):
        return {'BT2_INDEXES' : self.pipeline.host.get('bowtie2.index_dir')}

    def inputs(self):
        index_path=os.path.join(self.pipeline.host.get('bowtie2.index_dir'), self.ref_index)
        input1='%s_1.fastq' % self.data_basename
        input2='%s_2.fastq' % self.data_basename
        return [input1, input2] # skipping index_path for the moment; actually refers to lots of files

    def outputs(self):
        return ['%s.bt2.sam' % self.data_basename]
    
    
