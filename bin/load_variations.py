import sys, os, re, csv
libdir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','lib'))
sys.path.append(libdir)

from nof1_args import Nof1Args
import django_env
import django
from data.models import Variation
from dump_obj import dump

def main(args):
    '''
    load the variation data from one of three sources (LOVD, umd, or nhgri) 
    into the database.
    '''
    print args

    Variation.objects.filter(gene=args.gene, source=args.src).delete()
    stats={'n_vars':0}
    
    fn=get_fn(args)
    with open(fn) as f:
        reader=csv.reader(f, delimiter='\t')
        for line in reader:
            try:
                dnaVar=line[0]
                protVar=line[1]
                assay=line[2]
            except IndexError:
                continue
            var=Variation(dnaVariation=dnaVar, protVariation=protVar, assay=assay, gene=args.gene, source=args.src)
            var.save()
            stats['n_vars']+=1
    print dump(stats)

def get_fn(args):
    '''
    return the proper filename (data/variations/*.tsv) based on the args.gene and args.src value.
    '''
    src2fn={'lovd': 'LOVD.brca%d.tsv',
            'umd': 'umd.be.brca%d.causal.clean.tsv',
            'nhgri' : 'nhgri.brca%d_data.clean.tsv'}
    mg=re.search('^brca(\d)', args.gene, flags=re.I)
    if not mg:
        raise Exception('bad gene: %s' % args.gene)
    n_brca=int(mg.group(1))
    if n_brca != 1 and n_brca != 2:
        raise Exception('bad gene: %s' % args.gene)

    try:
        fn_format=src2fn[args.src.lower()]
    except KeyError:
        raise Exception('bad source: %s' % args.src)
        
    fn=os.path.join(args.root_dir, 'data', 'variations', fn_format % n_brca)
    return fn

if __name__=='__main__':
    config_fn=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'nof1.conf'))
    args=Nof1Args(config_fn, 'load on of the variations files into the db', 'load_variations')
    main(args.args)

