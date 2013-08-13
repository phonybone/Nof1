import os
from .run_cmd import RunCmd

class RunMuts2Vep(RunCmd):
    output_extension=".vep.in"

    '''
    sample input: data/trip_neg_Vic/triple_negativ_mut_seq.vep; used 
    bin/extract_trip_neg_details.py --in_fn data/trip_neg_Vic/triple_negativ_mut_seq
    to convert
    '''

    def __init__(self, host, working_dir, variants_fn):
        super(RunMuts2Vep, self).__init__('muts2vep', host, working_dir)
        self.variants_fn=variants_fn
        base=os.path.splitext(self.variants_fn)[0]
        self.out_fn=base+self.output_extension

    def get_cmd(self):
        return 'python'

    def get_args(self):
        cmd=[self.host.get('muts2vep.script'), 
             '-in_fn', self.variants_fn, 
             '-out_fn', self.out_fn]
        return cmd
    
    def outputs(self):
        return [self.out_fn]
