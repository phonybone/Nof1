import os, ConfigParser
from socket import gethostname


class RnaseqBranch(object):
    def __init__(self, data_basename, ref_index, conf):
        self.data_basename=data_basename
        self.ref_index=ref_index

        host=gethostname().split('.')[0]
        self.bt2_exe=conf.get(host, 'bowtie2.exe')
        self.bt2_index=conf.get(host, ref_index)
        self.n_procs=conf.get(host, 'n_procs')
        self.bowtie2_index_dir=conf.get(host, 'bowtie2.index_dir')
        self.rnaseq_count=conf.get(host, 'rnaseq_count')

    def run():
        self.run_bowtie2()
        (pid, status)=os.waitpid(pid, 0)
        if status!=0:
            print 'status=%d: bailing!' % status
            sys.exit(status)

        self.run_rnaseq_count()


    def run_bowtie2(self):
        input1='%s_1.fastq' % self.data_basename
        input2='%s_2.fastq' % self.data_basename
        output='%s.bt2.sam' % self.data_basename
        cmd=[self.ref_index, '-p', self.n_procs, 
             '-1' input1, '-2', input2, '-S', output]
        environ={'bt2_indexes' : bowtie2_index_dir}
        pid=os.fork()
        if pid==0:
            os.execve(self.bt2_exe, cmd, environ) # this should never return
            raise Exception('%s failed' % '\n'.join(cmd))

        return pid


    def run_rnaseq_count(self):
        input='%s.bt2.sam' % self.data_basename
        cmd=[self.rnaseq_count, '--in_fn', input]
        environ={}
        pid=os.fork()
        if pid==0:
            os.execve('python', cmd, environ) # this should never return
            raise Exception('%s failed' % '\n'.join(cmd))

        return pid
        
