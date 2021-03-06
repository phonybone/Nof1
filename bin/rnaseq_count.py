import sys, os, csv, re
libdir=os.path.abspath(os.path.join(os.path.dirname(__file__),'..','lib'))
print 'libdir is %s' % libdir
sys.path.append(libdir)

from nof1_args import Nof1Args
import django_env
from data.models import Knowngene
from pyBabel.SmartClient import SmartClient

def main(args):
    '''
    
    '''
    print args
#    if not args.out_fn:         # hack because this arg is necessary for all programs using nof1_args
#        print 'missing argument "--out_fn"'
#        sys.exit(1)

    ucsc2output=get_output_map(args.output_id_type)
    ucsc2count=read_ucsc(args)
    print '%d ucsc genes' % len(ucsc2count)

    gene2count=ucsc2gene(ucsc2count, ucsc2output)
    print '%d %s genes' % (len(gene2count), args.output_id_type)

    # write results:
    if args.out_fn:
        print 'writing results to %s...' % args.out_fn
        f=open(args.out_fn, 'w')
    else:
        f=sys.stdout

    for k in sorted(gene2count.keys()):
        f.write('%s: %d\n' % (k, gene2count[k]))

    if args.out_fn:
        f.close()

def get_output_map(output_type):
    client=SmartClient()
    client.load(['gene_known',output_type])
    return client.get_map('gene_known', output_type)

def read_ucsc(args):
    ''' 
    try to assign all alignments in input file to a gene via Knowngene lookup.
    could probably speed this up via smarter data structure (ie, not db look-ups).

    Input file is output of bowtie2, ie a .sam file
    '''
    print 'reading %s...' % args.in_fn

    n_alignments=0
    ucsc2count={'no_gene':0}
    with open(args.in_fn) as f:
        reader=csv.reader(f, delimiter='\t')
        for line in reader:
            if line[0].startswith('@'): continue
            chrom=line[2]
            pos=int(line[3])
            n_alignments+=1

            ucsc_genes=Knowngene.objects.filter(chrom=chrom, txstart__lte=pos, txend__gte=pos)
            if len(ucsc_genes)==0:
                ucsc2count['no_gene']+=1
                continue
            
            # populate ucsc2count:
            for name in [x.name for x in ucsc_genes]:
                try: ucsc2count[name]+=1
                except KeyError: ucsc2count[name]=1

    return ucsc2count

def ucsc2gene(ucsc2count, ucsc2output):
    ''' convert the ucsc2count table into gene2count: k=gene, v=count '''
    gene2count={}
    n_no_output_type=0

    for ucsc_id, count in ucsc2count.items():
        try: out_ids=ucsc2output[ucsc_id]  
        except KeyError:
            n_no_output_type+=1
            continue
            
        for out_id in out_ids:
            try: gene2count[out_id]+=count
            except KeyError: gene2count[out_id]=count
    return gene2count
            


    

if __name__=='__main__':
    config_fn=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'nof1.conf'))
    args=Nof1Args(config_fn, 'produce a list of expressed genes via a tag-counting approach', 'rnaseq_count')
    main(args.args)

