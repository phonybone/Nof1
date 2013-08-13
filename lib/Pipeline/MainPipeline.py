from Pipeline import Pipeline
from Pipeline.VEPBranch import VEPBranch
from Pipeline.RnaseqBranch import RnaseqBranch
from Pipeline.run_find_common import RunFindCommon

class MainPipeline(Pipeline):
    def __init__(self, host, working_dir, data_basename, ref_index, variants_fn):
        super(MainPipeline, self).__init__('Main', host, working_dir)
        self.data_basename=data_basename
        self.ref_index=ref_index
        self.variants_fn=variants_fn
        
        self.rnaseq=RnaseqBranch(self.host, self.working_dir, self.data_basename, self.ref_index)
        self.vep=VEPBranch(self.host, self.working_dir, self.variants_fn)

        fc_arg1={'fn':self.rnaseq.outputs()[0],
                 'alias':'rnaseq',
                 'field_no':1,
                 'delimiter':':'}
        fc_arg2={'fn':self.vep.outputs()[0],
                 'alias':'vep', 
                 'field_no':4}


        self.common=RunFindCommon(self.host, self.working_dir, [fc_arg1, fc_arg2])

    def run(self):
        self.rnaseq.run()
        self.vep.run()
        self.common.run()


        
