import sys, os, csv, re
libdir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','lib'))
sys.path.append(libdir)

from nof1_args import Nof1Args
import django_env
import django
from data.models import Knowngene


def main(args):
    '''
    
    '''
    print args
    ucsc2ll=read_ucsc2ll(args)
    ll2count=read_ucsc(args, ucsc2ll)

    out_fn=re.sub(r'bt2.sam$', 'genes.count', args.in_fn)
    special_ks={'n_alignments':None, 'no_gene':None, 'missing_ucsc':None, 'missing_ll':None, 'ambiguous':None}

    print 'out_fn: %s' % out_fn
    for k in sorted(ll2count.keys()):
        if k in special_ks: continue
        print '%s: %d' % (k, ll2count[k])

#    print ll2count
    for k in special_ks:
        print '%s: %d' % (k, ll2count[k])
    print 'found (lls): %d' % (len(ll2count)-len(special_ks))

def read_ucsc2ll(args):
    ucsc2ll={}
    with open(args.ucsc2ll) as f:
        reader=csv.reader(f, delimiter='\t')
        for line in reader:
            ucsc_id=line[0]
            ll_id=line[1]
            ucsc2ll[ucsc_id]=ll_id
    return ucsc2ll

def read_ucsc(args, ucsc2ll):
    ''' 
    try to assign all alignments in input file to a gene via Knowngene lookup.
    could probably speed this up via smarter data structure (ie, not db look-ups).

    Input file is output of bowtie2, ie a .sam file
    '''
    ll2count={'missing_ucsc':0, 'ambiguous':0, 'missing_ll':0, 'no_gene':0}
    fn=args.in_fn               # expects a .sam alignment file, as produced by bowtie[2]
    fuse=args.fuse
    n_alignments=0

    with open(fn) as f:
        reader=csv.reader(f, delimiter='\t')
        for line in reader:
            if line[0].startswith('@'): continue
            chrom=line[2]
            pos=int(line[3])
            n_alignments+=1

            genes=Knowngene.objects.filter(chrom=chrom, txstart__lte=pos, txend__gte=pos)
            if len(genes)==0:
                ll2count['no_gene']+=1
                continue

            lls=set()
            for g in genes:
                try:
                    ll_id=ucsc2ll[g.name]
                except KeyError:
                    ll2count['missing_ucsc']+=1
                    continue
                lls.add(ll_id)

            if len(lls) > 1:
                ll2count['ambiguous']+=1
                continue

            ll_list=list(lls)
            try: ll_id=ll_list[0]
            except IndexError: ll_id='missing_ll'

            try: ll2count[ll_id]+=1
            except KeyError: ll2count[ll_id]=1
                
            fuse-=1
            if fuse==0: break

    ll2count['n_alignments']=n_alignments
    return ll2count


    

if __name__=='__main__':
    config_fn=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'nof1.conf'))
    args=Nof1Args(config_fn, 'produce a list of expressed genes via a tag-counting approach', 'rnaseq_count')
    main(args.args)

