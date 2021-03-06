import os
from Pipeline.run_cmd import RunCmd

class RunMuts2Vep(RunCmd):
    auto_extension="auto"
    poly_extension="poly"
    '''
    sample input: data/trip_neg_Vic/triple_negativ_mut_seq.vep; used 
    bin/extract_trip_neg_details.py --in_fn data/trip_neg_Vic/triple_negativ_mut_seq
    to convert
    '''

    def __init__(self, pipeline, variants_fn, skip_if_current=False):
        super(RunMuts2Vep, self).__init__('muts2vep', pipeline, skip_if_current=skip_if_current)
        self.variants_fn=variants_fn
        base=os.path.splitext(self.variants_fn)[0]
        self.auto_fn='%s.%s' % (base,self.auto_extension)
        self.poly_fn='%s.%s' % (base,self.poly_extension)

    def get_cmd(self):
        return self.pipeline.host.get('python.exe')

    def get_args(self):
        cmd=[self.pipeline.host.get('muts2vep.script'), 
             '--in_fn', self.variants_fn, 
             '--auto_fn', self.auto_fn,
             '--poly_fn', self.poly_fn
             ]
        return cmd
    
    def inputs(self):
        return [self.variants_fn]

    def outputs(self):
        return [self.auto_fn, self.poly_fn]
