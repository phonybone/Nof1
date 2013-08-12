from .run_cmd import RunCmd

class RunRnaseqCount(RunCmd):
    def __init__(self, host, working_dir, data_basename):
        super(RunRnaseqCount, self).__init__('rnaseq_count', host, working_dir)
        self.data_basename=data_basename


    def get_cmd(self):
        return 'python'

    def get_args(self):
        input='%s_1.bt2.sam' % self.data_basename
        cmd=[self.host.get('rnaseq_count.script'), input]
        return cmd
    
    def get_environ(self):
        return {}
        
    
    
