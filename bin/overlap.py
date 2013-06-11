import sys, os
libdir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','lib'))
sys.path.append(libdir)

from nof1_args import Nof1Args
from dump_obj import dump
from uniprot2gene import uniprot2gene
from gene2synonym import gene2synonyms
from gene import readgenes

import django_env
import django
from data.models import Drug, DrugSynonym, DrugPathway, Target, TargetSynonym, TargetPathway

def main(args):
    print args

    # dump ttd targets and drugs:
    ttd_targets=Target.objects.filter(src='ttd')
    print 'ttd: %d targets' % len(ttd_targets)

    # dump drugbank targets
    db_targets=Target.objects.filter(src='db')
    print 'db: %d targets\n' % len(db_targets)

    # list shared targets in various ways
    shared('name')
    shared('gene_sym')
    shared('uniprot_id')
    
    # Look up Sam genes:
    genelist=readgenes(args.samgenes_fn)
    SamGenesWithUniprot(genelist, uniprot2gene(args.uniprot_gene_fn))
    SamGenes(genelist)

    # Look up tripNeg genes:
    genelist=readgenes(args.tripnegs_fn)
    g2s=gene2synonyms(args.gene2syn_fn)
    tripNegAll(genelist, g2s)
    

def shared(attr):
    ''' for a given attr,  '''
    ttd_genes=set([getattr(t,attr) for t in Target.objects.filter(src='ttd')])
    print '%d ttd unique %s' % (len(ttd_genes), attr)
    db_genes=set([getattr(t,attr) for t in Target.objects.filter(src='db')])
    print '%d drugbank unique %s' % (len(db_genes), attr)
    shared_genes=ttd_genes & db_genes
    print '%d shared %s\n' % (len(shared_genes), attr)

def SamGenesWithUniprot(genelist, u2g):
    ''' tabulate the sam genes that can have a uniprot associated with them '''
    stats={'n_found':0, 'n_missing':0, 'n_total':len(genelist)}
    for gene in genelist:
        try:
            u=u2g.g2u[gene]
            stats['n_found']+=1
        except KeyError:
            stats['n_missing']+=1
    print 'uniprot: %s' % dump(stats)

def SamGenes(genelist):
    ''' find the targets that have a sam gene associated with them (via gene_sym)  '''
    stats={'n_found':0, 'n_missing':0, 'n_total':len(genelist)}
    for gene in genelist:
        ttd_tars=Target.objects.filter(gene_sym=gene)
        if len(ttd_tars)>0:
#            print '%d targets for gene %s' % (len(ttd_tars), gene)
            stats['n_found']+=1
        else:
            stats['n_missing']+=1
    print 'SamGenes stats: %s' % dump(stats)


def tripNegAll(genelist, g2s):
    print 'trip_neg genes:'
    stats={'n_found':0, 'n_missing':0, 'n_total':len(genelist)}

    def get_targets(gene_syns):
        for gene in gene_syns:
            ts=Target.objects.filter(gene_sym=gene)
            if len(ts)>0:
                return ts, gene
        return [],None


    for gene in genelist:
        genes=[gene]
        try:
            syns=g2s.g2s[gene]
            genes.extend(syns)
        except KeyError: 
            pass
        ts, g2=get_targets(genes)
        if len(ts)>0:
            stats['n_found']+=1
        else:
            stats['n_missing']+=1

#        print '%d targets for %s (%s)' % (len(ts), genes, g2)
#        for t in ts:
#            print 'gene %s: target %s' % (gene, t)
    print 'tripNeg: %s' % dump(stats)

if __name__=='__main__':
    config_fn=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'nof1.conf'))
    args=Nof1Args(config_fn, 'look for overlap in drugbank/TTD', 'overlap')
    main(args.args)

