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
    genelist=readgenes(args.tripnegs_fn)
    print '%d trip-neg genes' % len(genelist)

    g2s=gene2synonyms(args.gene2syn_fn)

    def get_targets(gene_sym):
        genes=[gene_sym]
        try: genes.extend(g2s.g2s[gene_sym])
        except KeyError: pass
        targets=[]
        syms=[]
        for gene in genes:
            ts=Target.objects.filter(gene_sym=gene)
            if len(ts)>0:
                targets.extend(ts)
                syms.append(gene)
        return targets,syms


    for gene in genelist:
        targets=get_targets(gene)[0]
        if len(targets)>0:
            print 'gene %s: %d targets' % (gene, len(targets))
            for target in targets:
                drugs=target.drugs.all()
                print '  target: %s (%d drugs)' % (target, len(drugs))
                for drug in drugs:
                    print '    drug: %s' % drug
            print


if __name__=='__main__':
    config_fn=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'nof1.conf'))
    args=Nof1Args(config_fn, 'produce a report of all trip-neg genes, their targets, and drugs', 'gene_report')
    main(args.args)

