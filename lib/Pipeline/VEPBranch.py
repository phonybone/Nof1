from Pipeline import Pipeline
from .run_vep import RunVep
from .run_muts2vep import RunMuts2Vep
from .run_filter_vep import RunFilterVep

class VEPBranch(Pipeline):
    def __init__(self, host, working_dir, variants_fn, dry_run=False, output_dir=None):
        super(VEPBranch, self).__init__('VepBranch', host, working_dir, 
                                        dry_run, output_dir)
        self.variants_fn=variants_fn

        self.m2v=RunMuts2Vep(self, variants_fn)
        self.vep=RunVep(self, self.m2v.outputs()[1])
        self.filter_vep=RunFilterVep(self, self.vep.outputs()[0])

    def run(self):
        self.m2v.run()
        self.vep.run()
        self.filter_vep.run()

    def outputs(self):
        auto=self.m2v.outputs()[0]
        polyphen_sift_filtered=self.filter_vep.outputs()[0]
        return [auto, polyphen_sift_filtered]


                 
        
