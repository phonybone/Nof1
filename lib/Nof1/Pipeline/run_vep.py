import os
from .run_cmd import RunCmd
from socket import gethostname

class RunVep(RunCmd):
    output_extension=".vep.out"

    '''
    sample input: data/trip_neg_Vic/triple_negativ_mut_seq.vep; used 
    bin/extract_trip_neg_details.py --in_fn data/trip_neg_Vic/triple_negativ_mut_seq
    to convert
    '''

    def __init__(self, host, working_dir, variants_fn):
        super(RunVep, self).__init__('vep', host, working_dir)
        self.variants_fn=variants_fn

    def get_cmd(self):
        return 'perl'

    def get_args(self):
        output_fn=os.path.splitext(self.variants_fn)[0] + self.output_extension
        cmd=[self.host.get('vep.script'),
             '-i', self.variants_fn, 
             '--cache', 
             '--format', 'guess', 
             '--force_overwrite',
             '-o', output_fn]
        return cmd
    
    def get_environ(self):
        return {}
        
    
    
