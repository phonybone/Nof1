from drugcard import Drugcard
from drugtarget import DrugTarget
import re
from fysom import Fysom         # fsm library

class DrugbankReader(Fysom):
    def __init__(self, **kwargs):

        self.fn=kwargs['fn']
        self.builder=kwargs['builder']

        super(DrugbankReader, self).__init__({
                'initial': 'start',
                'events': [
                    {'src':'start',      'name':'begin_dc',  'dst':'def_dc'   },
                    {'src':'def_dc',     'name':'attr_name', 'dst':'wait_val' },
                    {'src':'wait_val',   'name':'value',     'dst':'assn_val' },
                    {'src':'wait_val',   'name':'seq_desc',  'dst':'assn_seqd'},
                    {'src':'assn_val',   'name':'value',     'dst':'assn_val' },
                    {'src':'assn_val',   'name':'end_dc',    'dst':'end_rec'  },
                    {'src':'assn_val',   'name':'attr_name', 'dst':'wait_val' },
                    {'src':'assn_val',   'name':'dtnan',     'dst':'wait_tval'},
                    {'src':'wait_tval',  'name':'value',     'dst':'assn_tval'},
                    {'src':'wait_tval',  'name':'seq_desc',  'dst':'assn_seqd'},
                    {'src':'assn_tval',  'name':'value',     'dst':'assn_tval'},
                    {'src':'assn_tval',  'name':'dtnan',     'dst':'wait_tval'},
                    {'src':'assn_tval',  'name':'end_dc',    'dst':'end_rec'  },
                    {'src':'assn_seqd',  'name':'seq',       'dst':'ext_seq'  },
                    {'src':'ext_seq',    'name':'seq',       'dst':'ext_seq'  },
                    {'src':'ext_seq',    'name':'begin_dc',  'dst':'def_dc'   },
                    {'src':'ext_seq',    'name':'attr_name', 'dst':'wait_val' },
                    {'src':'ext_seq',    'name':'dtnan',     'dst':'wait_tval'},
                    {'src':'end_rec',    'name':'begin_dc',  'dst':'def_dc'   },
                    ],
                'callbacks': {
                    'onbegin_dc' : self.builder.onbegin_dc,
                    'onattr_name': self.builder.onattr_name,
                    'onvalue'    : self.builder.onvalue,
                    'onseq_desc' : self.builder.onseq_desc,
                    'onseq'      : self.builder.onseq,
                    'onend_dc'   : self.builder.onend_dc,
                    'ondtnan'    : self.builder.ondtnan,

                    'onleave_ext_seq' : self.builder.onleave_ext_seq
                    }
                })

    def _line2event(self, line):
        for reg in self._line2event.regexs:
            mo=re.search(reg['regex'], line)
            if mo:
                return (reg['event'], mo)
        return (None,None)

    # order is important: most specific -> least specific
    _line2event.regexs=[{'regex':'^#BEGIN_DRUGCARD ([A-Z0-9]+)', 'event':'begin_dc'},
                        {'regex':'^#END_DRUGCARD ([A-Z0-9]+)',   'event':'end_dc'},
                        {'regex':'^# Drug_Target_(\d+)_(\S+):$', 'event':'dtnan'},
                        {'regex':'^# (.*):',                     'event':'attr_name'},
                        {'regex':'^>(.*)',                       'event':'seq_desc'},
                        {'regex':'^([A-Z]+)$',                   'event':'seq'},
                        {'regex':'(\S+)',                       'event':'value'}]

        
    def __iter__(self):
        ''' return the next Drugcard'''
        with open(self.fn) as f:
            dc=None
            cur_attr_name=None
            cur_target=None


            for line in f:
                event_name,mo=self._line2event(line)
                if not event_name: continue
                cb=getattr(self.builder,'on'+event_name)
                dc=cb(mo)
                if dc: 
                    yield dc

    

