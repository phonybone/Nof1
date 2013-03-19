from drugcard import Drugcard
from drugtarget import DrugTarget
from drugcard_builder import DrugcardBuilder
import rdf
from dump_obj import dump

class DrugcardBuilderRdf(DrugcardBuilder):
    def __init__(self):
        pass

    def onbegin_dc(self, mo):
        self.id=mo.group(1)
        self.dc=rdf.graph(id=self.id)
        self.current_sub=self.id
        self.current_graph=self.dc
        
    def onattr_name(self, mo):
        # check for existing seq:
        if (hasattr(self, 'sequence')) and (len(self.sequence) > 0):
            self.add_seq()

        self.current_attr_name=mo.group(1)

    def onvalue(self, mo):
        value=mo.group(1)
        trip=rdf.triple(sub=self.current_sub, pred=self.current_attr_name, obj=value)
        self.current_graph.add_triple(trip)

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
        dt_N=mo.group(1)
        dt_attr_name=mo.group(2)

        # check for self.sequence
        if hasattr(self, 'sequence') and len(self.sequence) > 0:
            self.add_seq()

        # init new dt if necessary:
#        if not hasattr(self, 'current_target') or self.current_target.N != dt_N:
        if not hasattr(self.current_graph, 'N') or self.current_graph.N != dt_N:
            target=rdf.graph()
            target.N=dt_N
            self.dc.add_triple(rdf.triple(sub=self.id, pred='has_target', obj=target))
            self.current_graph=target
            
        self.current_attr_name=dt_attr_name


    def onleave_ext_seq(self):
        print 'onleave_ext_seq '
        
    # this is a candidate for onleave_ext_seq callback
    def add_seq(self):
        edge=rdf.triple(sub=self.current_attr_name, pred=self.sequence_desc, obj=self.sequence)
        self.current_graph.add_triple(edge)

            
