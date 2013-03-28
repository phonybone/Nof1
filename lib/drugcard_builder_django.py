from uniprot2gene import uniprot2gene
from drugcard_builder import DrugcardBuilder

import django_env
import django
from data.models import Drug, DrugSynonym, DrugPathway, Target, TargetSynonym, TargetPathway

from dao_django import dao_django
from dump_obj import dump

class DrugcardBuilderDjango(DrugcardBuilder):
    attr_names={'Generic_Name':'name', # drugs
                'Primary_Accession_No':'primary_acc', # drugs
                'Drug_Type':'approval',               # drugs
                'ID':'id',      # targets
                'Name':'name',  # targets
                }

    def __init__(self, **kwargs):
        self.cur_obj=None
        self.cur_drug=None
        self.cur_target=None
        self.attr_name=None

        # clear tables if called for:
        if 'clear_table' in kwargs and kwargs['clear_table']:
            print 'clearing tables...'
            for cls in [ Drug, DrugSynonym, DrugPathway, Target, TargetSynonym, TargetPathway]:
                dao=dao_django(cls=cls)
                query = {'src':'db'} if cls==Drug or cls==Target else {}
                dao.remove(query)

        self.stats={'n_drugs':0,
                    'n_targets':0,
                    'n_drug_syns':0,
                    'n_target_syns':0,
                    'n_drug_pathways':0,
                    'n_target_pathways':0,
                    }

        self.ug=uniprot2gene(kwargs['uniprot_gene_fn'])




    def onbegin_dc(self, mo):
        id=mo.group(1)
        self.cur_drug=Drug(id=id, src='db')
#        self.cur_drug.save()
        self.cur_obj=self.cur_drug
        self.cur_target=None

    def onattr_name(self, mo):
        self.attr_name=mo.group(1)

    def onvalue(self, mo):
        value=mo.group(1)
        if self.attr_name in self.attr_names: 
            real_attr_name=self.attr_names[self.attr_name]
            setattr(self.cur_obj, real_attr_name, value)

        # Synonyms
        elif self.attr_name == 'Synonyms':
            if self.cur_target:
                syn=TargetSynonym(synonym=value, target=self.cur_target)
                self.cur_target.syns.append(syn)
            else:
                syn=DrugSynonym(synonym=value, drug=self.cur_drug)
                self.stats['n_drug_syns']+=1
                self.cur_obj.drugsynonym_set.add(syn)
                syn.save()


        # Gene_Name
        elif self.attr_name == 'Gene_Name':
            self.cur_target.gene_sym=value
            try:
                self.cur_target.uniprot_id=','.join(self.ug.g2u[value])
            except KeyError:
                pass
            

    '''
        # (Drug) Pathways
        elif self.attr_name == 'Pathways': # drug
            pathway=DrugPathway(name=value, drug=self.cur_drug)
            pathway.save()
            self.stats['n_drug_pathways']+=1

        # (Target) Pathway
        elif self.attr_name == 'Pathway': # target
            pathway=TargetPathway(name=value, target=self.cur_target)
            pathway.save()
            self.stats['n_target_pathways']+=1
    '''



    def onseq_desc(self, mo):
        pass                    # not interested

    def onseq(self, mo):
        pass                    # not interested

    def onend_dc(self, mo):
        self.cur_drug.save()
        self.stats['n_drugs']+=1
        print 'drug %s saved' % self.cur_drug.id

        if self.cur_target:
#            self.cur_target.save()
            self.save_target()
            self.cur_target.drugs.add(self.cur_drug)
            self.stats['n_targets']+=1

    def ondtnan(self, mo):
        dt_N=int(mo.group(1))
        dt_attr_name=mo.group(2)

        # Is this a new target?
        if not self.cur_target or self.target_n != dt_N:
            if self.cur_target:
#                self.cur_target.save() # re-save, really
                self.save_target()
                self.cur_drug.save()
                self.cur_target.drugs.add(self.cur_drug)
                self.stats['n_targets']+=1

            self.cur_target=Target(src='db')
            self.cur_target.syns=[]
            self.cur_obj=self.cur_target
            self.target_n=dt_N
        self.attr_name=dt_attr_name

    def onleave_ext_seq(self):
        pass

    '''
    def save_drug(self):
        self.cur_drug.save()
        for target in self.targets:
            target.drugs.add(self.cur_drug)
            target.save()

    '''
    def save_target(self):
        if not hasattr(self.cur_target, 'id'):
            raise Exception('target has no id: %s' % self.cur_target)
#        self.cur_target.save()
#        print '%s saved' % self.cur_target
        for s in self.cur_target.syns:
            syn=TargetSynonym(synonym=s, target=self.cur_target)
            self.cur_target.targetsynonym_set.add(syn)
        self.cur_target.save()
        print '%s saved' % self.cur_target

