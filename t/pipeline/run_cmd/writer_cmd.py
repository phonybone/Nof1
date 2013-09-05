import os, sys
root_dir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','..','..'))
sys.path.append(os.path.join(root_dir, 'lib'))

from Pipeline.run_cmd import RunCmd

class writer_cmd(RunCmd):
    def get_cmd(self): 
        return 'python'
    def get_args(self): 
        return [os.path.join(os.path.dirname(__file__), 'writer.py')]
    def get_environ(self): 
        return {}
    def outputs(self): return []
    
