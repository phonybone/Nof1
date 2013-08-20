import os
from .run_cmd import RunCmd

class RunMuts2Vep(RunCmd):
    auto_extension="auto"
    poly_extension="poly"
    '''
    sample input: data/trip_neg_Vic/triple_negativ_mut_seq.vep; used 
    bin/extract_trip_neg_details.py --in_fn data/trip_neg_Vic/triple_negativ_mut_seq
    to convert
    '''

    def __init__(self, host, working_dir, variants_fn):
        super(RunMuts2Vep, self).__init__('muts2vep', host, working_dir)
        self.variants_fn=variants_fn
        base=os.path.splitext(self.variants_fn)[0]
        self.auto_fn='%s.%s' % (base,self.auto_extension)
        self.poly_fn='%s.%s' % (base,self.poly_extension)

    def get_cmd(self):
        return 'python'

    def get_args(self):
        cmd=[self.host.get('muts2vep.script'), 
             '--in_fn', self.variants_fn, 
             '--auto_fn', self.auto_fn,
             '--poly_fn', self.poly_fn
             ]
        return cmd
    
    def outputs(self):
        return [self.auto_fn, self.poly_fn]
