import os
from .run_cmd import RunCmd
from .exceptions import MissingArgs

class RunFindCommon(RunCmd):
    output_extension="common"
    '''
    find_common test_rnaseq/rawdata/1047-COPD.10K.genes.count,rnaseq,1,: trip_neg_Vic/triple_negativ_mut_seq.vep.out,vep,4
    '''
    def __init__(self, pipeline, fc_args, arg_delim=',', skip_if_current=False):
        '''
        each fc_arg must be a dict containing the following keys: fn, alias, field_no, delimiter
        defaults exist (in find_common) for alias (fn), field_no (None), and delimiter (None)

        This has been deprecated in favor of run_combine.py
        '''
        super(RunFindCommon, self).__init__('find_common', pipeline, skip_if_current=skip_if_current)
        self.arg_delim=arg_delim

        self.fc_args=fc_args
        if len(self.fc_args)==0:
            raise MissingArgs('fc_args')

    def get_cmd(self):
        return self.pipeline.host.get('find_common.script')

    def get_args(self):
        args=['--out_fn', self.outputs()[0]]
        for arg in self.fc_args:
            l=[]
            for k in ['fn', 'alias', 'field_no', 'delimiter']:
                try: l.append(str(arg[k]))
                except KeyError: pass
            args.append(self.arg_delim.join(l))
        return args
                    
    
    def get_environ(self):
        return {}
        
    def inputs(self):
        return [k[fn] for k in self.fc_args]

    def outputs(self):
        l=[os.path.basename(a['fn'].split('.')[0]) for a in self.fc_args]
        return [os.path.join(self.pipeline.working_dir, '%s.%s' % ('_'.join(l), self.output_extension))]
