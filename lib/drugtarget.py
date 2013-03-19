class DrugTarget(object):
    _save_keys=['__all__']

    def __init__(self, N, **kwargs):
        self.N=N
        self.seqs={}
        self.__dict__.update(kwargs)

    def add_attr(self, attr, val):
        if not hasattr(self, attr):
            setattr(self, [])
        getattr(self, attr).append(val)
        
    def add_seq(self, attr_name, seq_desc, seq):
        self.seqs[seq_desc]=seq


