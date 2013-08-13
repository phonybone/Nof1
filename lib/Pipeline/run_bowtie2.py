from .run_cmd import RunCmd

class RunBowtie2(RunCmd):
    def __init__(self, host, working_dir, data_basename, ref_index):
        super(RunBowtie2, self).__init__('bowtie2', host, working_dir)
        self.data_basename=data_basename
        self.ref_index=ref_index


    def get_cmd(self):
        return self.host.get('bowtie2.exe')

    def get_args(self):
        input1='%s_1.fastq' % self.data_basename
        input2='%s_2.fastq' % self.data_basename
        output=self.outputs()[0]
        cmd=[self.ref_index, 
             '-p', self.host.get('n_procs'),
             '-1', input1, 
             '-2', input2, 
             '-S', output]
        return cmd
    
    def get_environ(self):
        return {'bt2_indexes' : self.host.get('bowtie2.index_dir')}

    def outputs(self):
        return '%s.bt2.sam' % self.data_basename
    
    
