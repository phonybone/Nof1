from .run_cmd import RunCmd
from socket import gethostname

class RunBowtie2(RunCmd):
    def __init__(self, data_basename, ref_index, conf):
        self.data_basename=data_basename
        self.ref_index=ref_index

        host=gethostname().split('.')[0]
        self.cmd=conf.get(host, 'bowtie2.exe')
        self.ref_index=ref_index
        self.n_procs=conf.get(host, 'n_procs')
        self.bowtie2_index_dir=conf.get(host, 'bowtie2.index_dir')

    def get_cmd(self):
        return self.cmd

    def get_args(self):
        input1='%s_1.fastq' % self.data_basename
        input2='%s_2.fastq' % self.data_basename
        output='%s.bt2.sam' % self.data_basename
        cmd=[self.ref_index, '-p', self.n_procs, 
             '-1', input1, '-2', input2, '-S', output]
        return cmd
    
    def get_environ(self):
        return {'bt2_indexes' : bowtie2_index_dir}
        
    
    
