import os
from Pipeline.run_cmd import RunCmd

class RunVep(RunCmd):
    output_extension=".vep.out"

    '''
    sample input: data/trip_neg_Vic/triple_negativ_mut_seq.vep; used 
    bin/extract_trip_neg_details.py --in_fn data/trip_neg_Vic/triple_negativ_mut_seq
    to convert
    '''

    def __init__(self, pipeline, variants_fn, skip_if_current=False):
        super(RunVep, self).__init__('vep', pipeline, skip_if_current=skip_if_current)
        self.variants_fn=variants_fn

    def get_cmd(self):
        return self.pipeline.host.get('perl.exe')

    def get_args(self):
        output_fn=self.outputs()[0]
        cmd=[self.pipeline.host.get('vep.script'),
             '-i', self.variants_fn, 
             '--cache', 
             '--format', 'guess', 
             '--force_overwrite',
             '--poly', 'p',
             '--sift', 'p',
             '-o', output_fn]
        return cmd

    def inputs(self):
        return [self.variants_fn]

    def outputs(self):
        return [os.path.splitext(self.variants_fn)[0] + self.output_extension] # also a .html file!
    
    
