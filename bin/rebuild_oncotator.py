import sys, os, requests

libdir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','lib'))
sys.path.append(libdir)
from nof1_args import Nof1Args
import django_env
import django
from data.models import OncotatorGene, UniprotProtein
from gene import readgenes
import json
from dao_django import dao_django
from dump_obj import dump

def main(args):
    print args

    # clear dbs:
    if False:
        dao_og=dao_django(cls=OncotatorGene)
        dao_og.remove({})
        dao_op=dao_django(cls=UniprotProtein)
        dao_op.remove({})

    genes=readgenes(args.in_fn)
    base_url=args.base_url
    stats={'n_genes':0, 'n_prots':0}

    for gn in genes:
        try:
            gene=OncotatorGene.objects.get(name=gn)
            print '%s: already loaded' % gn
            continue
        except OncotatorGene.DoesNotExist:
            pass
            
        url=base_url+gn
        res=requests.get(url)
        if res.status_code != 200:
            print '%s: error/nothing found' % gn
            continue
        print gn
        
        dct=json.loads(res.content)
#        for k,v in dct.items():
#            print '%s: %s' % (k,v)
        gene=OncotatorGene(name=gn, 
                           full_name=dct['full_name'], 
                           chr=dct['chr'],
                           location=dct['location'],
                           start=dct['start'],
                           end=dct['end'],
                           strand=dct['strand'])
        gene.save()
        stats['n_genes']+=1
        prot_accs=[dct['uniprot_accession']]
        try:
            prot_accs.extend(dct['alt_uniprot_accessions'])
        except KeyError:
            pass
        for acc in prot_accs:
            prot=UniprotProtein(id=acc, gene=gene)
            prot.save()
            stats['n_prots']+=1

    print dump(stats)



if __name__=='__main__':
    config_fn=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'nof1.conf'))
    args=Nof1Args(config_fn, 'do something with oncotator', 'oncotator')
    main(args.args)

