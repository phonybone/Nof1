from Pipeline import Pipeline
from .run_vep import RunVep
from .run_muts2vep import RunMuts2Vep
from .run_filter_vep import RunFilterVep

class VEPBranch(Pipeline):
    def __init__(self, host, working_dir, variants_fn, 
                 dry_run=False, output_dir=None, echo=False, skip_if_current=False):
        super(VEPBranch, self).__init__('VepBranch', host, working_dir, 
                                        output_dir=output_dir, dry_run=dry_run, echo=echo,
                                        skip_if_current=skip_if_current)
        self.variants_fn=variants_fn

        self.m2v=RunMuts2Vep(self, variants_fn, skip_if_current)
        self.vep=RunVep(self, self.m2v.outputs()[1], skip_if_current)
        self.filter_vep=RunFilterVep(self, self.vep.outputs()[0], skip_if_current)

    def run(self):
        self._run_cmds(self.m2v, 
                       self.vep, 
                       self.filter_vep)

    def outputs(self):
        auto=self.m2v.outputs()[0]
        polyphen_sift_filtered=self.filter_vep.outputs()[0]
        return [auto, polyphen_sift_filtered]


                 
        
