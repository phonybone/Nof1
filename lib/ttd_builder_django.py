import sys, os, re
from uniprot2gene import uniprot2gene

import django_env
import django
from data.models import Drug, DrugSynonym, DrugPathway, Target, TargetSynonym, TargetPathway

from dump_obj import dump

class TtdBuilderDjango(object):
    
    def __init__(self, **kwargs):
        self.db_name=kwargs['db']
        self.cur_target=None
        self.cur_id=None
        self.targets=[]

        # fixme: all of this should really be in the dao_django class
        if 'clear_table' in kwargs and kwargs['clear_table']:
            print 'clearing tables...'
            for cls in [ Drug, DrugSynonym, DrugPathway, Target, TargetSynonym, TargetPathway]:
                objs=cls.objects.all()
                try:
                    objs.delete()
                except django.db.utils.DatabaseError:
                    print 'clearing objects the long way for %s' % cls.__name__
                    for o in objs:
                        o.delete()

        self.stats={'n_drugs':0,
                    'n_targets':0,
                    'n_pathways':0}

        self.ug=uniprot2gene(kwargs['uniprot_gene_fn'])

    # These are called by the reader
    def on_line3(self, row):
        self._common(row)
    
    def on_line4(self, row):
        self._common(row)
    
    def on_line6(self, row):
        self._common(row)
        
    def on_eof(self):
        self.cur_target.save()
        self.stats['n_targets']+=1
        return self.targets

    def _common(self, row):
        '''
        do things common to line[346]: 
        - check for new target (via id), save old target;
        - do the method name lookup, and call it
        '''
        id=row[0]
        if id != self.cur_id:
            if self.cur_target:
                print '_common: about to save target: %s: %d drugs, %d synonyms, %d pathways' % \
                    (self.cur_target.id,
                     len(self.cur_target.drugs.all()),
                     len(self.cur_target.targetsynonym_set.all()),
                     len(self.cur_target.targetpathway_set.all()))
                self.cur_target.save()
                self.stats['n_targets']+=1
            self.cur_target=Target(id=id, src='ttd')
            self.cur_target.save() # to get id; will re-save later
            self.cur_id=id
            self.targets.append(self.cur_target)

        method_name=self.sanitize(row[1])
        try:
            method=getattr(self, 'on_'+method_name)
            method(row)
        except AttributeError:
            pass

    def sanitize(self, method_name):
        return re.sub('\W', '', method_name)


    def on_Name(self, row):
        self.cur_target.name=row[2]

    def on_Synonyms(self, row):
        syn=TargetSynonym(synonym=row[2], target=self.cur_target)
        syn.save()
        self.cur_target.synonyms.add(syn)

    def on_Drugs(self, row):
        if row[5] not in Drug.approvals: 
#            print 'not approved: %s' % '\t'.join(row)
            return
        drug=Drug(id=row[3], name=row[2], condition=row[4], approval=row[5], src='ttd')
        drug.save()
        self.stats['n_drugs']+=1
        self.cur_target.drugs.add(drug)

    def on_Pathway(self, row):
        pw=TargetPathway(name=row[2], target=self.cur_target)
        pw.save()
        self.stats['n_pathways']+=1
        self.cur_target.targetpathways.add(pw)

    def on_UniProtID(self, row):
        self.cur_target.uniprot_id=row[2]
        try:
            gs=self.ug.u2g[row[2]]
            self.cur_target.gene_sym=','.join(gs)
        except KeyError:
            print 'no genes found for uniprot=%s' % row[2]
