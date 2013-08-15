from Pipeline import Pipeline
from Pipeline.run_vep import RunVep
from Pipeline.run_muts2vep import RunMuts2Vep

class VEPBranch(Pipeline):
    def __init__(self, host, working_dir, variants_fn):
        super(VEPBranch, self).__init__('VepBranch', host, working_dir)
        self.variants_fn=variants_fn

        self.m2v=RunMuts2Vep(self.host, self.working_dir, self.variants_fn)
        self.vep=RunVep(self.host, self.working_dir, self.m2v.outputs()[1])
        self.filter_vep=RunFilterVep(self.host, self.working_dir, self.vep.outputs()[0])

    def run(self):
        self.m2v.run()
        self.vep.run()
        self.filter_vep.run()

    def outputs(self):
        return self.filter_vep.outputs()


                 
        
