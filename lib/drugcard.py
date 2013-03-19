class Drugcard(object):
    _save_keys=['__all__']

    def __init__(self, **kwargs):
        self.id=kwargs['id']    # explicit test to insure existance
        self.targets=[]
        self.seqs={}
        self.__dict__.update(**kwargs)

    def add_attr(self, attr, val):
        if not hasattr(self, attr):
            setattr(self, [])
        getattr(self, attr).append(val)
        
    def add_target(self, target):
        self.targets.append(target)

    def add_seq(self, attr_name, seq_desc, seq):
        self.seqs[seq_desc]=seq # attr_name unused???

    def cur_target(self):       # this probably shouldn't be here (used by dc_b_report.py)
        try:
            return self.targets[-1]
        except IndexError:
            return None

        
