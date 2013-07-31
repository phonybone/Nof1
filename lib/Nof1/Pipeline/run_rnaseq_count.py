from .run_cmd import RunCmd

class RunBowtie(RunCmd):
    def __init__(self, data_basename, conf):
        self.data_basename=data_basename

        host=gethostname().split('.')[0]
        self.cmd=conf.get(host, 'rnaseq_count')

    def get_cmd(self):
        return self.cmd

    def get_args(self):
        input='%s_1.bt2.sam' % self.data_basename
        cmd=[input]
        return cmd
    
    def get_environ(self):
        return {}
        
    
    
