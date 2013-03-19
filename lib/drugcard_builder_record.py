from drugcard import Drugcard
from drugtarget import DrugTarget
from drugcard_builder import DrugcardBuilder

class DrugcardBuilderRecord(DrugcardBuilder):
    def __init__(self):
        pass

    def onbegin_dc(self, mo):
        dc_id=mo.group(1)
        self.dc=Drugcard(id=dc_id)
        self.cur_obj=self.dc

    def onattr_name(self, mo):
        # check for existing seq:
        if (hasattr(self, 'sequence')) and (len(self.sequence) > 0):
            self.add_seq()

        self.attr_name=mo.group(1)
        if not hasattr(self.cur_obj, self.attr_name):
            setattr(self.cur_obj, self.attr_name, [])

    def onvalue(self, mo):
        value=mo.group(1)
        getattr(self.cur_obj, self.attr_name).append(value)

    def onseq_desc(self, mo):
        # check for existing seq:
        if hasattr(self, 'sequence') and len(self.sequence) > 0:
            self.add_seq()

        # could come from within attr_name or dtnan:
        self.sequence_desc=mo.group(1)
        self.sequence=''

    def onseq(self, mo):
        self.sequence+=mo.group(1)

    def onend_dc(self, mo):
        return self.dc

    def ondtnan(self, mo):
        # check for self.sequence
        if hasattr(self, 'sequence') and len(self.sequence) > 0:
            self.add_seq()

        dt_N=mo.group(1)
        dt_attr_name=mo.group(2)

        # init new dt if necessary:
        if not self.dc.cur_target() or self.dc.cur_target().N != dt_N:
            self.cur_obj=DrugTarget(dt_N)
            self.dc.add_target(self.cur_obj)
            
        self.attr_name=dt_attr_name
        if not hasattr(self.cur_obj, self.attr_name):
            setattr(self.cur_obj, self.attr_name, [])


    def onleave_seq_ext(self):
        print 'onleave_seq_ext called'
        
    # this is a candidate for onleave_ext_seq callback
    def add_seq(self):
        self.cur_obj.add_seq(self.attr_name, self.sequence_desc, self.sequence)
            
